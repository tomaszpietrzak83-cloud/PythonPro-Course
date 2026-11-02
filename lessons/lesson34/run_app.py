"""Start or restart only the server owned by this lesson."""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / ".runtime"


def stop_previous(pidfile):
    """A saved PID may have been reused; verify age before reading its command."""
    import psutil

    try:
        old = json.loads(pidfile.read_text(encoding="utf-8"))
        process = psutil.Process(int(old["pid"]))
        if abs(process.create_time() - float(old["created"])) >= 1:
            return  # This PID now belongs to another process.
        if str(ROOT / "app.py") not in process.cmdline():
            return
        children = process.children(recursive=True)
        for child in reversed(children):
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        process.terminate()
        _, alive = psutil.wait_procs(children + [process], timeout=5)
        for remaining in alive:
            try:
                remaining.kill()
            except psutil.NoSuchProcess:
                pass
    except psutil.NoSuchProcess:
        pass
    except psutil.AccessDenied:
        print(
            "Windows odmówił dostępu do zapisanego procesu. Pomijam jego zamykanie i sprawdzam port lekcji."
        )
    except (OSError, ValueError, KeyError, TypeError):
        print(
            "Pomijam nieaktualny lub uszkodzony zapis procesu w .runtime/server.json."
        )


def port_available():
    """Never mistake an unrelated service for a successfully started lesson."""
    with socket.socket() as probe:
        if os.name == "nt":
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        try:
            probe.bind(("127.0.0.1", 8034))
        except OSError:
            return False
    return True


def main():
    shared = ROOT / ".venv" / "Scripts" / "python.exe"
    if shared.exists() and Path(sys.executable).resolve() != shared.resolve():
        return subprocess.call(
            [
                str(shared),
                str(Path(__file__).resolve()),
                *sys.argv[1:],
            ]
        )
    from curriculum import ensure_material

    try:
        if ensure_material():
            print("Zaktualizowano objaśnienia po zmianie formatowania kodu.")
    except (ValueError, OSError, SyntaxError) as error:
        print(f"Nie można wczytać materiałów: {error}")
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    # Use this lesson’s isolated environment, also when launched by course Python.
    python = ROOT / ".venv" / "Scripts" / "python.exe"
    if not python.exists():
        python = Path(sys.executable)
    RUNTIME.mkdir(exist_ok=True)
    pidfile = RUNTIME / "server.json"
    if pidfile.exists():
        stop_previous(pidfile)
    if not port_available():
        print(
            "Port 8034 jest zajęty. Zamknij poprzedni serwer lekcji lub program używający tego portu i uruchom ponownie."
        )
        return 1
    log = (RUNTIME / "server.log").open("a", encoding="utf-8")
    creation = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    process = subprocess.Popen(
        [str(python), str(ROOT / "app.py")],
        cwd=ROOT,
        stdout=log,
        stderr=log,
        creationflags=creation,
    )
    import psutil

    pidfile.write_text(
        json.dumps(
            {
                "pid": process.pid,
                "created": psutil.Process(process.pid).create_time(),
            }
        )
    )
    for _ in range(60):
        if process.poll() is not None:
            print("Nie udało się uruchomić. Sprawdź .runtime/server.log.")
            return 1
        try:
            with urllib.request.urlopen("http://127.0.0.1:8034/api/course", timeout=1):
                break
        except urllib.error.HTTPError as error:
            if error.code >= 500:
                process.terminate()
                print(
                    f"Serwer działa, ale wczytanie lekcji zwróciło HTTP {error.code}. Sprawdź .runtime/server.log."
                )
                return 1
            time.sleep(0.25)
        except OSError:
            time.sleep(0.25)
    else:
        process.terminate()
        print("Serwer nie odpowiedział. Sprawdź .runtime/server.log.")
        return 1
    print("Lekcja 34: http://127.0.0.1:8034/")
    print("Realtime Studio — 20 zadań, analiza kodu i rzeczywiste wyniki.")
    if not args.no_browser:
        webbrowser.open("http://127.0.0.1:8034/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
