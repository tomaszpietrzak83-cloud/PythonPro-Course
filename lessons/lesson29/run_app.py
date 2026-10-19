"""Start Docker/Redis, a Celery worker, Django and the browser for lesson 29."""

import argparse
import errno
import hashlib
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONTAINER = "lesson29-redis"


def is_lesson_running(url):
    identity = hashlib.sha256(
        str(BASE.resolve()).casefold().encode()
    ).hexdigest()
    try:
        with urllib.request.urlopen(url + "health/", timeout=2) as response:
            data = json.load(response)
        return (
            data.get("app") == "lesson29" and data.get("workspace") == identity
        )
    except (OSError, ValueError, AttributeError):
        return False


def stop_previous_instance(url, port):
    """Ask this workspace's launcher to terminate its own child processes."""
    stop_file = BASE / ".runtime" / f"stop-{port}"
    stop_file.parent.mkdir(parents=True, exist_ok=True)
    stop_file.write_text("restart", encoding="utf-8")
    print("Zatrzymuję poprzednią aplikację i jej usługi...", flush=True)
    deadline = time.monotonic() + 35
    while time.monotonic() < deadline:
        if not stop_file.exists():
            with socket.socket() as probe:
                try:
                    probe.bind(("127.0.0.1", port))
                    return
                except OSError:
                    pass
        time.sleep(0.25)
    raise RuntimeError(
        "Poprzednia aplikacja nie zakończyła pracy. Zamknij jej terminal i spróbuj ponownie."
    )


def docker(*args, check=True, timeout=15):
    return subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        check=check,
        timeout=timeout,
    )


def start_redis():
    if not shutil.which("docker"):
        raise RuntimeError(
            "Docker Desktop is missing. Install it, or use --local-queue."
        )
    if docker("info", check=False).returncode:
        desktop = (
            Path(os.environ.get("ProgramFiles", "C:/Program Files"))
            / "Docker/Docker/Docker Desktop.exe"
        )
        if not desktop.exists():
            raise RuntimeError("Open Docker Desktop and retry.")
        # Start the background desktop service without opening a console window.
        startup = subprocess.STARTUPINFO() if os.name == "nt" else None
        if startup:
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup.wShowWindow = 0
        subprocess.Popen(
            [str(desktop)],
            startupinfo=startup,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        print("Waiting for Docker Desktop (up to 90 seconds)...", flush=True)
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if docker("info", check=False).returncode == 0:
                break
            time.sleep(2)
        else:
            raise RuntimeError(
                "Docker did not become ready. Open Docker Desktop or use --local-queue."
            )
    existing = docker("container", "inspect", CONTAINER, check=False)
    if existing.returncode:
        print("Creating the lesson29 Redis container...", flush=True)
        docker(
            "run",
            "-d",
            "--name",
            CONTAINER,
            "-p",
            "127.0.0.1:6389:6379",
            "redis:7-alpine",
            timeout=180,
        )
    else:
        docker("start", CONTAINER)
    import redis

    client = redis.Redis(
        host="127.0.0.1", port=6389, socket_connect_timeout=1, socket_timeout=1
    )
    for _ in range(30):
        try:
            if client.ping():
                return
        except redis.RedisError:
            time.sleep(0.5)
    raise RuntimeError("Redis did not respond on localhost:6389.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local-queue",
        action="store_true",
        help="Use a real filesystem Celery queue without Docker",
    )
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--port", type=int, default=8029)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port musi mieścić się w zakresie 1–65535.")
    missing = [
        name
        for name in (
            "django",
            "celery",
            "redis",
            "pygments",
            "bs4",
            "PIL",
            "requests",
            "flower",
        )
        if importlib.util.find_spec(name) is None
    ]
    if missing:
        python = BASE.parents[1] / ".venv/Scripts/python.exe"
        if (
            python.exists()
            and Path(sys.executable).resolve() != python.resolve()
        ):
            return subprocess.call(
                [str(python), str(Path(__file__).resolve()), *sys.argv[1:]]
            )
        raise RuntimeError(
            "Missing libraries. Run: python -m pip install -r lessons/lesson29/requirements.txt"
        )
    url = f"http://127.0.0.1:{args.port}/"
    try:
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", args.port))
    except OSError as error:
        if (
            error.errno != errno.EADDRINUSE
            and getattr(error, "winerror", None) != 10048
        ):
            raise
        if is_lesson_running(url):
            stop_previous_instance(url, args.port)
        else:
            raise RuntimeError(
                f"Port {args.port} jest zajęty przez inną aplikację. Wybierz inny port, np. --port 8030."
            ) from error
    env = os.environ.copy()
    if args.local_queue:
        env["LESSON29_BROKER_URL"] = "filesystem://"
        env.pop("LESSON29_RESULT_BACKEND", None)
    else:
        start_redis()
        env["LESSON29_BROKER_URL"] = "redis://127.0.0.1:6389/0"
        env["LESSON29_RESULT_BACKEND"] = "redis://127.0.0.1:6389/1"
    env["PYTHONUNBUFFERED"] = "1"
    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        cwd=BASE,
        env=env,
        check=True,
    )
    subprocess.run(
        [sys.executable, "manage.py", "seed_lesson"],
        cwd=BASE,
        env=env,
        check=True,
    )
    env["FLOWER_UNAUTHENTICATED_API"] = "true"
    children = []
    stop_file = BASE / ".runtime" / f"stop-{args.port}"
    stop_file.unlink(missing_ok=True)
    log_handles = []
    original_popen = subprocess.Popen

    def logged_process(command, **kwargs):
        service = (
            "django"
            if "manage.py" in command
            else (
                "priority"
                if "priority_queue" in command
                else (
                    "beat"
                    if "beat" in command
                    else "flower" if "flower" in command else "worker"
                )
            )
        )
        handle = (BASE / ".runtime" / f"{service}.log").open(
            "a", encoding="utf-8"
        )
        log_handles.append(handle)
        return original_popen(
            command, stdout=handle, stderr=subprocess.STDOUT, **kwargs
        )

    try:
        # TASK 18
        worker = logged_process(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "academy",
                "worker",
                "--pool=solo",
                "--concurrency=1",
                "-l",
                "info",
                "--hostname=lesson29-default@%h",
                "-Q",
                "default",
                "-E",
            ],
            cwd=BASE,
            env=env,
        )
        children.append(worker)
        # Wait for an actual worker response before making the UI available.
        env["DJANGO_SETTINGS_MODULE"] = "academy.settings"
        os.environ.update(
            {
                key: env[key]
                for key in ("LESSON29_BROKER_URL", "DJANGO_SETTINGS_MODULE")
            }
        )
        if "LESSON29_RESULT_BACKEND" in env:
            os.environ["LESSON29_RESULT_BACKEND"] = env[
                "LESSON29_RESULT_BACKEND"
            ]
        else:
            os.environ.pop("LESSON29_RESULT_BACKEND", None)
        from academy.celery import app

        for _ in range(15):
            if worker.poll() is not None:
                raise RuntimeError(
                    "The Celery worker stopped. Check .runtime/worker.log."
                )
            if app.control.ping(timeout=1):
                break
        else:
            raise RuntimeError("The Celery worker did not become ready.")
        # TASK 18
        priority = logged_process(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "academy",
                "worker",
                "--pool=solo",
                "--concurrency=1",
                "-l",
                "info",
                "--hostname=lesson29-priority@%h",
                "-Q",
                "priority_queue",
                "-E",
            ],
            cwd=BASE,
            env=env,
        )
        children.append(priority)
        # TASK 04
        # TASK 06
        # TASK 12
        # TASK 13
        beat = logged_process(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "academy",
                "beat",
                "-l",
                "info",
                "--schedule",
                str(BASE / ".runtime/celerybeat"),
            ],
            cwd=BASE,
            env=env,
        )
        children.append(beat)
        # TASK 19
        flower = logged_process(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "academy",
                "flower",
                "--address=127.0.0.1",
                "--port=5559",
            ],
            cwd=BASE,
            env=env,
        )
        children.append(flower)
        for _ in range(30):
            if any(child.poll() is not None for child in children):
                raise RuntimeError("A service stopped. See .runtime/*.log.")
            ready_workers = app.control.ping(timeout=1)
            try:
                with urllib.request.urlopen(
                    "http://127.0.0.1:5559/", timeout=1
                ) as response:
                    flower_ready = response.status == 200
            except (OSError, urllib.error.URLError):
                flower_ready = False
            if len(ready_workers) >= 2 and flower_ready:
                break
        else:
            raise RuntimeError(
                "The second worker or Flower did not become ready. See .runtime/*.log."
            )
        server = logged_process(
            [
                sys.executable,
                "manage.py",
                "runserver",
                f"127.0.0.1:{args.port}",
                "--noreload",
            ],
            cwd=BASE,
            env=env,
        )
        children.append(server)
        url = f"http://127.0.0.1:{args.port}/"
        for _ in range(60):
            if server.poll() is not None:
                raise RuntimeError("Django stopped before becoming ready.")
            try:
                with urllib.request.urlopen(url, timeout=1) as response:
                    if response.status == 200:
                        break
            except (OSError, urllib.error.URLError):
                time.sleep(0.25)
        else:
            raise RuntimeError("The web server did not become ready.")
        print(
            f"\nCelery Lab: {url}\nCtrl+C stops Django and the worker. Redis stays available.\n",
            flush=True,
        )
        if not args.no_browser:
            webbrowser.open(url)
        while all(child.poll() is None for child in children):
            if stop_file.exists():
                print("Restart: zatrzymuję poprzednie procesy.", flush=True)
                return 0
            time.sleep(0.5)
        raise RuntimeError(
            "A service stopped unexpectedly. See the console output."
        )
    except KeyboardInterrupt:
        print("\nStopping lesson 29...")
    finally:
        for child in reversed(children):
            if child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
        for handle in log_handles:
            handle.close()
        stop_file.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from course_runtime import use_course_python
    use_course_python(__file__)
    try:
        sys.exit(main() or 0)
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(f"\nCould not start lesson 29: {error}", file=sys.stderr)
        sys.exit(1)
