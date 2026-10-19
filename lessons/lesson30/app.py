"""Local Django UI. Every demonstration runs in an isolated subprocess."""
import atexit
import json
import math
import os
import platform
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

from django.conf import settings

ROOT = Path(__file__).resolve().parent
if not settings.configured:
    settings.configure(
        DEBUG=False, SECRET_KEY="local-lesson30-only",
        ROOT_URLCONF=__name__, ALLOWED_HOSTS=["127.0.0.1", "localhost", "testserver"],
        MIDDLEWARE=["django.middleware.csrf.CsrfViewMiddleware"],
        TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [ROOT / "templates"], "APP_DIRS": False}],
        DEFAULT_CHARSET="utf-8")

import django

django.setup()
from curriculum import ROOT, lesson
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

JOBS = {}
JOB_LOCK = threading.Lock()
IMAGE = "lesson30-python:local"


def validate(number, data):
    if not isinstance(data, dict):
        raise ValueError("Dane muszą być obiektem / inputs must be an object")
    limits = {7: ("number", -1000, 1000), 9: ("size", 4, 10_000_000),
              12: ("size", 100_000, 20_000_000), 19: ("workers", 1, 10),
              20: ("side", 20, 1000)}
    allowed = {n: {v[0]} for n, v in limits.items()}
    allowed.update({8: {"name"}, 10: {"word"}, 17: {"numbers"}})
    if set(data) - allowed.get(number, set()):
        raise ValueError("Nieznane pole / unknown field")
    if number in limits:
        key, low, high = limits[number]
        if key in data and (type(data[key]) is not int or not low <= data[key] <= high):
            raise ValueError(f"{key}: {low} … {high}")
    for key in ("name", "word"):
        if key in data and (not isinstance(data[key], str) or
                            not 1 <= len(data[key].strip()) <= 80):
            raise ValueError(f"{key}: 1 … 80 znaków / characters")
    if number == 17 and "numbers" in data:
        values = data["numbers"]
        if (not isinstance(values, list) or not 1 <= len(values) <= 100 or
            any(type(x) not in (int, float) or not math.isfinite(x)
                or abs(x) > 1e9 for x in values)):
            raise ValueError("numbers: 1–100 skończonych liczb / finite numbers")
    return data


def command(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=8, **kwargs)


def resources():
    docker = {"installed": bool(shutil.which("docker")), "ready": False,
              "image": False}
    if docker["installed"]:
        try:
            result = command(["docker", "info", "--format", "{{.OSType}}"])
            docker["ready"] = result.returncode == 0 and "linux" in result.stdout
            if docker["ready"]:
                docker["image"] = command(["docker", "image", "inspect", IMAGE]).returncode == 0
            else:
                docker["message"] = (result.stderr or result.stdout)[-300:]
        except (OSError, subprocess.TimeoutExpired) as error:
            docker["message"] = str(error)
    return dict(python=sys.version.split()[0], system=platform.system(),
                cores=os.cpu_count(), gil=getattr(sys, "_is_gil_enabled", lambda: True)(),
                docker=docker)


def stop_job(job):
    process = job.get("process")
    if not process or process.poll() is not None:
        return
    job["cancelled"] = True
    if job["backend"] == "docker":
        try:
            command(["docker", "rm", "-f", job["container"]])
        except (OSError, subprocess.TimeoutExpired):
            pass
    elif os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       capture_output=True, timeout=10)
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        process.kill()


def execute(job):
    args = [sys.executable, "-u", str(ROOT / "examples" / f"task{job['number']:02}.py")]
    env = dict(os.environ, LESSON30_INPUT=json.dumps(job["input"]),
               PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    if job["backend"] == "docker":
        args = ["docker", "run", "--rm", "--name", job["container"],
                "--network", "none", "--cpus", "2", "--memory", "2g",
                "--pids-limit", "64", "--read-only", "--tmpfs", "/tmp:size=512m",
                "--label", f"lesson30.server={os.getpid()}",
                "--mount", f"type=bind,source={ROOT / 'examples'},target=/lesson/examples,readonly",
                "-e", "LESSON30_INPUT=" + json.dumps(job["input"]), IMAGE,
                "python", "-u", f"/lesson/examples/task{job['number']:02}.py"]
    timer = None
    try:
        process = subprocess.Popen(args, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True,
                                   encoding="utf-8", errors="replace",
                                   start_new_session=os.name != "nt")
        job["process"] = process
        timer = threading.Timer(180, lambda: stop_job(job))
        timer.daemon = True
        timer.start()
        for line in process.stdout:
            try:
                item = json.loads(line)
                if not isinstance(item, dict) or "kind" not in item:
                    raise ValueError("non-event")
            except (ValueError, json.JSONDecodeError):
                item = dict(kind="log", actor="stderr", label=line.rstrip(),
                            at=time.perf_counter())
            with JOB_LOCK:
                if len(job["events"]) < 2500:
                    job["events"].append(item)
        code = process.wait()
        job["status"] = ("cancelled" if job.get("cancelled") else
                         "done" if code == 0 and not any(
                             e["kind"] == "error" for e in job["events"]) else "error")
        job["exitcode"] = code
    except Exception as error:
        job["status"] = "error"
        job["events"].append(dict(kind="error", actor="launcher", label=str(error),
                                  at=time.perf_counter()))
    finally:
        if timer:
            timer.cancel()
        job["finished"] = time.time()


@ensure_csrf_cookie
def index(request):
    version = max(p.stat().st_mtime_ns for p in (ROOT / "static").iterdir())
    return render(request, "index.html", {"version": version})


def course(request):
    lessons = [lesson(n) for n in range(1, 21)]
    for item in lessons:
        # Code and annotations must be delivered from the SAME source snapshot.
        item["steps"]["rows"] = highlighted_rows(item["steps"]["source"])
    response = JsonResponse({"lessons": lessons})
    response["Cache-Control"] = "no-store"
    return response


def highlighted_rows(source):
    formatter = HtmlFormatter(nowrap=True)
    return [highlight(row, PythonLexer(), formatter).rstrip("\n")
            for row in source.splitlines()]


def code(request, number):
    if not 1 <= number <= 20:
        return JsonResponse({"error": "Unknown task"}, status=404)
    name = "lab_support.py" if request.GET.get("helper") == "1" else f"task{number:02}.py"
    source = (ROOT / "examples" / name).read_text(encoding="utf-8")
    # Highlight each physical row independently so line numbers always match source.
    response = JsonResponse(dict(file=name, rows=highlighted_rows(source), source=source))
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
        if backend not in ("native", "docker"):
            raise ValueError("Unknown backend")
        if backend == "docker":
            state = resources()["docker"]
            if not state["ready"] or not state["image"]:
                raise ValueError("Włącz Docker i zbuduj obraz według README / start Docker and build the image")
    except (ValueError, AttributeError, TypeError) as error:
        return JsonResponse({"error": str(error)}, status=400)
    with JOB_LOCK:
        if any(j["status"] == "running" for j in JOBS.values()):
            return JsonResponse({"error": "Trwa pokaz / a demonstration is running"}, status=409)
        # Keep the last 30 runs; do not grow memory indefinitely.
        for key in list(JOBS)[:-29]:
            del JOBS[key]
        key = uuid.uuid4().hex
        job = dict(id=key, number=number, input=data, backend=backend,
                   container="lesson30-" + key, events=[], status="running")
        JOBS[key] = job
    threading.Thread(target=execute, args=(job,), daemon=True).start()
    return JsonResponse({"id": key}, status=202)


def status(request, key):
    with JOB_LOCK:
        job = JOBS.get(key)
        if not job:
            return JsonResponse({"error": "Unknown run"}, status=404)
        return JsonResponse({k: job[k] for k in ("id", "number", "backend", "input", "events", "status")})


def cancel(request, key):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    job = JOBS.get(key)
    if not job:
        return JsonResponse({"error": "Unknown run"}, status=404)
    stop_job(job)
    return JsonResponse({"ok": True})


def cleanup():
    for job in list(JOBS.values()):
        stop_job(job)


atexit.register(cleanup)
urlpatterns = [path("", index), path("api/course", course),
               path("api/resources", lambda r: JsonResponse(resources())),
               path("api/code/<int:number>", code), path("api/run/<int:number>", run),
               path("api/status/<str:key>", status), path("api/cancel/<str:key>", cancel),
               path("static/<path:path>", serve, {"document_root": ROOT / "static"})]


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line([__file__, "runserver", "127.0.0.1:8030", "--noreload"])
