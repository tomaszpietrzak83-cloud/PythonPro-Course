"""Uruchomienie niezależnego laboratorium; bez Dockera i bez GameShelf."""

import argparse
import os
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def free_port(port):
    """Zakończ proces nasłuchujący na wybranym porcie przed startem."""
    if sys.platform == "win32":
        lookup = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
             f"Get-NetTCPConnection -State Listen -LocalPort {port} "
             "-ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique"],
            capture_output=True, text=True,
        )
    else:
        lookup = subprocess.run(
            ["lsof", "-t", f"-iTCP:{port}", "-sTCP:LISTEN"],
            capture_output=True, text=True,
        )
    owners = {int(line.strip()) for line in lookup.stdout.splitlines() if line.strip().isdigit()}
    for pid in owners:
        if pid in (0, os.getpid(), os.getppid()):
            raise RuntimeError(f"Nie można zakończyć procesu {pid} na porcie {port}.")
        print(f"Zwalniam port {port}: zatrzymuję proces {pid}.", flush=True)
        if sys.platform == "win32":
            stopped = subprocess.run(
                ["taskkill.exe", "/PID", str(pid), "/F"], capture_output=True, text=True,
            )
            if stopped.returncode:
                raise RuntimeError(f"Nie udało się zakończyć procesu {pid}: {stopped.stderr.strip() or stopped.stdout.strip()}")
        else:
            os.kill(pid, signal.SIGKILL)
    for _ in range(40):
        try:
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", port))
            return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Port {port} nadal jest niedostępny. Sprawdź uprawnienia procesu.")


def open_when_ready(url):
    for _ in range(60):
        try:
            with urllib.request.urlopen(url + "health/", timeout=1) as response:
                if response.status == 200:
                    webbrowser.open(url)
                    return
        except OSError:
            time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="API Lab · Lekcja 28")
    parser.add_argument("--port", type=int, default=8028)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port musi mieścić się w zakresie 1–65535.")
    try:
        import django  # noqa: F401
        import drf_spectacular
        import drf_spectacular_sidecar
        import pygments
        import rest_framework
    except ImportError as error:
        print(
            f"Brak biblioteki: {error.name}. Zainstaluj requirements.txt tego projektu."
        )
        return 1
    try:
        free_port(args.port)
    except (OSError, RuntimeError) as error:
        print(f"Nie udało się zwolnić portu: {error}")
        return 1
    command = [sys.executable, str(BASE_DIR / "manage.py")]
    for action in (["migrate", "--noinput"], ["seed_lab"], ["check"]):
        subprocess.run(command + action, cwd=BASE_DIR, check=True)
    url = f"http://127.0.0.1:{args.port}/"
    print(f"API Lab: {url}\nCtrl+C zatrzymuje serwer.", flush=True)
    if not args.no_browser:
        threading.Thread(
            target=open_when_ready, args=(url,), daemon=True
        ).start()
    server = subprocess.Popen(
        command + ["runserver", f"127.0.0.1:{args.port}", "--noreload"],
        cwd=BASE_DIR,
    )
    try:
        return server.wait()
    except KeyboardInterrupt:
        if server.poll() is None:
            server.terminate()
        server.wait()
        return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from course_runtime import use_course_python
    use_course_python(__file__)
    local_python = BASE_DIR.parents[2] / (
        ".venv/Scripts/python.exe"
        if sys.platform == "win32"
        else ".venv/bin/python"
    )
    if (
        local_python.exists()
        and Path(sys.executable).resolve() != local_python.resolve()
    ):
        try:
            raise SystemExit(
                subprocess.call(
                    [
                        str(local_python),
                        str(Path(__file__).resolve()),
                        *sys.argv[1:],
                    ],
                    cwd=BASE_DIR,
                )
            )
        except KeyboardInterrupt:
            raise SystemExit(0)
    raise SystemExit(main())
