"""Start the control panel and three Django servers; Ctrl+C shuts them down."""

import argparse
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.request import urlopen

LESSON = Path(__file__).resolve().parent.parent
PROJECTS = (("l27_pro", 8000), ("l27_pro_2", 8001), ("l27_pro_3", 8002))


def demo_environment(project):
    """Create a persistent demo copy using SQLite's consistent backup API."""
    runtime = Path(__file__).resolve().parent / "runtime"
    runtime.mkdir(exist_ok=True)
    target = runtime / f"{project}.sqlite3"
    source = LESSON / project / "db.sqlite3"
    if not target.exists() and source.exists():
        with sqlite3.connect(f"{source.as_uri()}?mode=ro", uri=True) as original:
            with sqlite3.connect(target) as duplicate:
                original.backup(duplicate)
    return {**os.environ, "LESSON27_DEMO_DATABASE": str(target), "PYTHONUNBUFFERED": "1"}


def port_available(port):
    with socket.socket() as probe:
        try:
            probe.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


def redis_available():
    try:
        import redis
        from redis.backoff import NoBackoff
        from redis.retry import Retry
        return redis.Redis(host="127.0.0.1", port=6379, socket_connect_timeout=1,
                           socket_timeout=1, retry=Retry(NoBackoff(), 0)).ping()
    except Exception:
        return False


def prepare_redis():
    """Use an existing Redis service, or start the lesson's named container."""
    if redis_available():
        print("Redis is already available on port 6379.", flush=True)
        return True
    docker = shutil.which("docker")
    if not docker:
        candidates = [Path("C:/Program Files/Docker/Docker/resources/bin/docker.exe"),
                      Path.home() / "AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe"]
        docker = next((str(path) for path in candidates if path.exists()), None)
    if not docker:
        print("Redis unavailable. Install/start Docker Desktop or start Redis separately.", flush=True)
        return False
    try:
        engine = subprocess.run([docker, "info"], capture_output=True, timeout=8)
        if engine.returncode:
            print("Docker engine unavailable. Open Docker Desktop, then restart this launcher.", flush=True)
            return False
        container = subprocess.run([docker, "container", "inspect", "redis-cache"], capture_output=True, timeout=8)
        command = [docker, "start", "redis-cache"] if container.returncode == 0 else [
            docker, "run", "--name", "redis-cache", "-p", "6379:6379", "-d", "redis:7-alpine"]
        result = subprocess.run(command, timeout=45)
        if result.returncode:
            return False
        for _ in range(10):
            if redis_available():
                return True
            time.sleep(.5)
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"Redis startup failed: {type(error).__name__}", flush=True)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-browser", action="store_true", help="Do not open the browser automatically.")
    parser.add_argument("--skip-redis-start", action="store_true", help="Check Redis without starting Docker containers.")
    parser.add_argument("--no-autostart", action="store_true", help="Open Home with all three Django servers initially stopped.")
    args = parser.parse_args()
    # Recognize our existing controller before checking Django ports. Pressing
    # Play again should print its link, rather than create duplicate processes.
    sys.path.insert(0, str(LESSON))
    from cache_demo.controller import CONTROL_PORT, ProcessManager, create_controller
    address = f"http://127.0.0.1:{CONTROL_PORT}/"
    if not port_available(CONTROL_PORT):
        try:
            with urlopen(address + "control/status/", timeout=2) as response:
                if response.headers.get("X-Lesson27-Controller") == "CacheLab":
                    print(f"Cache Lab is already running: {address}", flush=True)
                    if not args.no_browser:
                        webbrowser.open(address)
                    return
        except OSError:
            pass
        raise SystemExit(f"Control port {CONTROL_PORT} is occupied by another service.")
    occupied = [port for _, port in PROJECTS if not port_available(port)]
    if occupied:
        raise SystemExit(f"Ports already occupied: {occupied}. Stop those servers before starting the presentation.")
    redis_ready = redis_available() if args.skip_redis_start else prepare_redis()
    if not redis_ready:
        print("Tasks 1–9 remain available. Task 10 will show a real Redis connection error.", flush=True)
    # The launcher remains alive as a small control service even when every
    # Django process is stopped. Home is therefore always able to restart them.
    manager = ProcessManager(demo_environment, port_available)
    controller = create_controller(manager)
    try:
        if not args.no_autostart:
            for project, _ in PROJECTS:
                manager.start(project)
        if not args.no_browser:
            webbrowser.open(address)
        print(f"Control panel ready: {address}", flush=True)
        print("Use runserver / Stop server on Home. Ctrl+C stops the launcher and its Django servers.", flush=True)
        controller.serve_forever(poll_interval=.5)
    except KeyboardInterrupt:
        print("Stopping the control panel and Django servers...", flush=True)
    finally:
        controller.server_close()
        manager.stop_all()
        # Redis is reusable lesson infrastructure and is left running.


if __name__ == "__main__":
    main()
