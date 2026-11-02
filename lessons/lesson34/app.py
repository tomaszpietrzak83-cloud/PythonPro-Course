"""Local asyncio teaching studio; isolated demonstration subprocesses."""

import atexit
import json
import os
import platform
import signal
import subprocess
import sys
import threading
import time
import urllib.request
import uuid
from pathlib import Path

from django.conf import settings

ROOT = Path(__file__).resolve().parent
if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY="local-lesson34-only",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["127.0.0.1", "localhost", "testserver"],
        MIDDLEWARE=["django.middleware.csrf.CsrfViewMiddleware"],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [ROOT / "templates"],
                "APP_DIRS": False,
            }
        ],
        DEFAULT_CHARSET="utf-8",
    )

import django

django.setup()
from curriculum import ROOT, ensure_material, lesson, task_sources
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

JOBS = {}
JOB_LOCK = threading.Lock()
DOCS_LOCK = threading.Lock()
DOCS_JOB = {}


def validate(number, data):
    if not isinstance(data, dict):
        raise ValueError("Inputs must be an object")
    if data:
        raise ValueError("This demonstration uses prepared inputs")
    return data


def resources():
    return dict(
        python=sys.version.split()[0],
        system=platform.system(),
        cores=os.cpu_count(),
        gil=getattr(sys, "_is_gil_enabled", lambda: True)(),
        mode="aiohttp / Strawberry / SQLite",
    )


def stop_job(job):
    job["cancelled"] = True
    process = job.get("process")
    if not process or process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            timeout=10,
        )
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()


def execute(job):
    args = [
        sys.executable,
        "-u",
        str(ROOT / "examples" / "run_task.py"),
        str(job["number"]),
    ]
    env = dict(
        os.environ,
        LESSON34_INPUT=json.dumps(job["input"]),
        PYTHONIOENCODING="utf-8",
        PYTHONUNBUFFERED="1",
    )
    timer = None
    try:
        process = subprocess.Popen(
            args,
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=os.name != "nt",
        )
        job["process"] = process
        if job.get("cancelled"):
            stop_job(job)
        timer = threading.Timer(180, lambda: stop_job(job))
        timer.daemon = True
        timer.start()
        for line in process.stdout:
            try:
                item = json.loads(line)
                if not isinstance(item, dict) or "kind" not in item:
                    raise ValueError("non-event")
            except (ValueError, json.JSONDecodeError):
                item = dict(
                    kind="log",
                    actor="stderr",
                    label=line.rstrip(),
                    at=time.perf_counter(),
                )
            with JOB_LOCK:
                if len(job["events"]) < 2500:
                    job["events"].append(item)
        code = process.wait()
        job["status"] = (
            "cancelled"
            if job.get("cancelled")
            else "done"
            if code == 0 and not any(e["kind"] == "error" for e in job["events"])
            else "error"
        )
        job["exitcode"] = code
    except Exception as error:
        job["status"] = "error"
        job["events"].append(
            dict(
                kind="error",
                actor="launcher",
                label=str(error),
                at=time.perf_counter(),
            )
        )
    finally:
        if timer:
            timer.cancel()
        job["finished"] = time.time()


@ensure_csrf_cookie
def index(request):
    version = max(p.stat().st_mtime_ns for p in (ROOT / "static").iterdir())
    return render(request, "index.html", {"version": version})


def course(request):
    try:
        ensure_material()
    except (ValueError, OSError, SyntaxError) as error:
        import logging

        logging.getLogger(__name__).exception("Unable to load lesson material")
        return JsonResponse({"error": str(error)}, status=503)
    lessons = [lesson(n) for n in range(1, 21)]
    for item in lessons:
        # Code and annotations must be delivered from the SAME source snapshot.
        item["steps"]["rows"] = highlighted_rows(item["steps"]["source"])
        for source in item["steps"]["sources"].values():
            source["rows"] = highlighted_rows(source["source"])
    response = JsonResponse({"lessons": lessons})
    response["Cache-Control"] = "no-store"
    return response


def highlighted_rows(source):
    formatter = HtmlFormatter(nowrap=True)
    return [
        highlight(row, PythonLexer(), formatter).rstrip("\n")
        for row in source.splitlines()
    ]


def code(request, number):
    if not 1 <= number <= 20:
        return JsonResponse({"error": "Unknown task"}, status=404)
    name = request.GET.get("file") or "main.py"
    sources = task_sources(number)
    if name not in sources:
        return JsonResponse({"error": "Unknown source file"}, status=404)
    source = sources[name]
    # Highlight each physical row independently so line numbers always match source.
    response = JsonResponse(
        dict(file=name, rows=highlighted_rows(source), source=source)
    )
    response["Cache-Control"] = "no-store"
    return response


def run(request, number):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not 1 <= number <= 20:
        return JsonResponse({"error": "Unknown task"}, status=404)
    try:
        body = json.loads(request.body)
        data = validate(number, body.get("input", {}))
        backend = body.get("backend", "native")
        if backend != "native":
            raise ValueError("Only local Python is supported")
    except (ValueError, AttributeError, TypeError) as error:
        return JsonResponse({"error": str(error)}, status=400)
    with JOB_LOCK:
        if any(j["status"] == "running" for j in JOBS.values()):
            return JsonResponse(
                {"error": "Trwa pokaz / a demonstration is running"}, status=409
            )
        # Keep the last 30 runs; do not grow memory indefinitely.
        for key in list(JOBS)[:-29]:
            del JOBS[key]
        key = uuid.uuid4().hex
        job = dict(
            id=key,
            number=number,
            input=data,
            backend=backend,
            events=[],
            status="running",
        )
        JOBS[key] = job
    threading.Thread(target=execute, args=(job,), daemon=True).start()
    return JsonResponse({"id": key}, status=202)


def status(request, key):
    with JOB_LOCK:
        job = JOBS.get(key)
        if not job:
            return JsonResponse({"error": "Unknown run"}, status=404)
        return JsonResponse(
            {
                k: job[k]
                for k in ("id", "number", "backend", "input", "events", "status")
            }
        )


def cancel(request, key):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    job = JOBS.get(key)
    if not job:
        return JsonResponse({"error": "Unknown run"}, status=404)
    stop_job(job)
    return JsonResponse({"ok": True})


def graphql_ide(request, number):
    if number not in {4, 5, 6, 10, 12, 15, 17, 19}:
        return JsonResponse({"error": "Unknown task"}, status=404)
    with DOCS_LOCK:
        process = DOCS_JOB.get("process")
        version = max(
            p.stat().st_mtime_ns
            for p in (ROOT / "examples" / f"task{number:02}").rglob("*.py")
        )
        if (
            process
            and process.poll() is None
            and DOCS_JOB.get("number") == number
            and DOCS_JOB.get("version") == version
        ):
            return HttpResponseRedirect("http://127.0.0.1:8134/graphql")
        if process and process.poll() is None:
            stop_job(DOCS_JOB)
            process.wait(timeout=10)
        # Refuse to terminate or reuse an unrelated service occupying the docs port.
        import socket

        try:
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", 8134))
        except OSError:
            return JsonResponse(
                {"error": "Port 8134 is busy. Close the previous GraphiQL server."},
                status=409,
            )
        runtime = ROOT / ".runtime"
        runtime.mkdir(exist_ok=True)
        with (runtime / "graphql.log").open("a", encoding="utf-8") as log:
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(ROOT / "examples" / "run_task.py"),
                    str(number),
                    "--serve",
                ],
                cwd=ROOT,
                stdout=log,
                stderr=log,
                env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                start_new_session=os.name != "nt",
            )
        DOCS_JOB.clear()
        DOCS_JOB.update(process=process, number=number, version=version)
        for _ in range(100):
            if process.poll() is not None:
                break
            try:
                with urllib.request.urlopen(
                    "http://127.0.0.1:8134/__ready", timeout=0.3
                ) as response:
                    json.load(response)
                return HttpResponseRedirect("http://127.0.0.1:8134/graphql")
            except OSError:
                time.sleep(0.1)
        stop_job(DOCS_JOB)
        return JsonResponse(
            {"error": "GraphiQL startup failed; see .runtime/graphql.log"},
            status=503,
        )


def cleanup():
    for job in list(JOBS.values()):
        stop_job(job)
    stop_job(DOCS_JOB)


atexit.register(cleanup)
from eleven_narration import audio_view, config_view, generate_view

urlpatterns = [
    path("", index),
    path("api/course", course),
    path("api/narration/config", config_view),
    path("api/narration/generate", generate_view),
    path("api/narration/audio/<str:digest>", audio_view),
    path("api/docs/<int:number>", graphql_ide),
    path("api/resources", lambda r: JsonResponse(resources())),
    path("api/code/<int:number>", code),
    path("api/run/<int:number>", run),
    path("api/status/<str:key>", status),
    path("api/cancel/<str:key>", cancel),
    path("static/<path:path>", serve, {"document_root": ROOT / "static"}),
]


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(
        [
            __file__,
            "runserver",
            "127.0.0.1:8034",
            "--noreload",
        ]
    )
