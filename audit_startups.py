"""Launch isolated copies of Django projects and check local HTTP responses."""

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = {
    **os.environ,
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUNBUFFERED": "1",
    "DJANGO_SECRET_KEY": "audit-local-only",
    "POSTGRES_PASSWORD": "audit-local-only",
}
RESULTS = []


def smoke(base, label, launcher=None):
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    if launcher:
        code = (
            "import sys,runpy; sys.path.insert(0,"
            + repr(
                str(base.parents[2] if label == "API Lab" else base.parents[1])
            )
            + '); import course_runtime; course_runtime.PYTHON=__import__("pathlib").Path(sys.executable); runpy.run_path("run_app.py",run_name="__main__")'
        )
        args = [
            sys.executable,
            "-c",
            code,
            "--no-browser",
            "--port",
            str(port),
            *launcher,
        ]
    else:
        source = (base / "manage.py").read_text(encoding="utf-8")
        settings = re.search(r"[\"\']([\w.]+\.settings)[\"\']", source).group(1)
        (base / "audit_settings.py").write_text(
            f"from {settings} import *\nDATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': r'{base / 'audit.sqlite3'}'}}}}\nALLOWED_HOSTS = ['localhost','127.0.0.1','testserver']\nCACHES = {{'default': {{'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}}}\n",
            encoding="utf-8",
        )
        init = subprocess.run(
            [
                sys.executable,
                "manage.py",
                "migrate",
                "--noinput",
                "--settings",
                "audit_settings",
            ],
            cwd=base,
            env=ENV,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if init.returncode:
            return {
                "test": label,
                "status": "FAIL",
                "output": init.stdout + init.stderr,
            }
        args = [
            sys.executable,
            "manage.py",
            "runserver",
            f"127.0.0.1:{port}",
            "--noreload",
            "--settings",
            "audit_settings",
        ]
    log = base / "audit-start.log"
    with log.open("w", encoding="utf-8") as handle:
        process = subprocess.Popen(
            args, cwd=base, env=ENV, stdout=handle, stderr=subprocess.STDOUT
        )
        result = {"test": label, "status": "FAIL"}
        try:
            for _ in range(100 if launcher else 40):
                if process.poll() is not None:
                    break
                try:
                    with urllib.request.urlopen(
                        f"http://127.0.0.1:{port}/", timeout=1
                    ) as response:
                        result = {
                            "test": label,
                            "status": "PASS",
                            "http": response.status,
                        }
                        break
                except urllib.error.HTTPError as error:
                    result = {
                        "test": label,
                        "status": "PASS" if error.code < 500 else "FAIL",
                        "http": error.code,
                    }
                    break
                except OSError:
                    time.sleep(0.3)
            if label == "Celery Lab" and result["status"] == "PASS":
                task_env = {**ENV, "LESSON29_BROKER_URL": "filesystem://"}
                task_env.pop("LESSON29_RESULT_BACKEND", None)
                task = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        "from academy.celery import app; result=app.send_task('learning.tasks.multiply',args=[6,7]); value=result.get(timeout=12); print(value); assert value==42",
                    ],
                    cwd=base,
                    env=task_env,
                    capture_output=True,
                    text=True,
                    timeout=18,
                )
                result["task_result"] = task.stdout.strip()
                if task.returncode:
                    result["status"] = "FAIL"
                    result["task_error"] = task.stderr
        finally:
            if launcher and label == "Celery Lab":
                (base / ".runtime").mkdir(exist_ok=True)
                (base / ".runtime" / f"stop-{port}").touch()
                try:
                    process.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    pass
            if process.poll() is None:
                import psutil

                children = psutil.Process(process.pid).children(recursive=True)
                process.terminate()
                for child in children:
                    try:
                        child.terminate()
                    except psutil.NoSuchProcess:
                        pass
                process.wait(timeout=5)
            result["output"] = log.read_text(
                encoding="utf-8", errors="replace"
            )[-5000:]
            if label == "Celery Lab" and result["status"] == "FAIL":
                for child_log in (base / ".runtime").glob("*.log"):
                    result["output"] += (
                        "\n"
                        + child_log.name
                        + "\n"
                        + child_log.read_text(
                            encoding="utf-8", errors="replace"
                        )[-6000:]
                    )
        return result


(ROOT / ".audit-temp").mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(
    prefix="startup-", dir=ROOT / ".audit-temp"
) as folder:
    temp = Path(folder)
    shutil.copytree(
        ROOT / "lessons",
        temp / "lessons",
        ignore=shutil.ignore_patterns(
            ".venv",
            ".env",
            ".env.*",
            "__pycache__",
            ".runtime",
            "*.sqlite3",
            "media",
        ),
    )
    shutil.copy2(ROOT / "course_runtime.py", temp / "course_runtime.py")
    projects = (
        []
        if "--only-celery" in sys.argv
        else list((temp / "lessons").glob("*/*/manage.py"))
        + [temp / "lessons/lesson29/manage.py"]
    )
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [
            pool.submit(smoke, p.parent, str(p.parent.relative_to(temp)))
            for p in projects
        ]
        for job in jobs:
            r = job.result()
            RESULTS.append(r)
            print(r["test"], r["status"], r.get("http"), flush=True)
    for label, relative, options in [
        ("API Lab", "lesson28/api_lab", []),
        ("Celery Lab", "lesson29", ["--local-queue"]),
    ]:
        if "--only-celery" in sys.argv and label != "Celery Lab":
            continue
        if label == "Celery Lab":
            # Isolate the auxiliary Flower port from any user's running service.
            p = temp / "lessons" / relative / "run_app.py"
            p.write_text(
                p.read_text(encoding="utf-8").replace("5559", "15559"),
                encoding="utf-8",
            )
        r = smoke(temp / "lessons" / relative, label, options)
        RESULTS.append(r)
        print(label, r["status"], r.get("http"), flush=True)
(
    ROOT
    / (
        "celery-startup-results.json"
        if "--only-celery" in sys.argv
        else "startup-results.json"
    )
).write_text(
    json.dumps(RESULTS, ensure_ascii=False, indent=2), encoding="utf-8"
)
for r in RESULTS:
    if r["status"] == "FAIL":
        print(r["test"], r["output"])
