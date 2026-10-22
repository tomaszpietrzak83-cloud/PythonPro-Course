"""Start or restart only the server owned by this lesson."""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / ".runtime"


def main():
    shared = ROOT.parents[1] / ".venv" / "Scripts" / "python.exe"
    if shared.exists() and Path(sys.executable).resolve() != shared.resolve():
        return subprocess.call(
            [str(shared), str(Path(__file__).resolve()), *sys.argv[1:]]
        )
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    # Shared course environment, including when launched by a system Python.
    python = ROOT.parents[1] / ".venv" / "Scripts" / "python.exe"
    if not python.exists():
        python = Path(sys.executable)
    RUNTIME.mkdir(exist_ok=True)
    pidfile = RUNTIME / "server.json"
    if pidfile.exists():
        old = json.loads(pidfile.read_text())
        # Verify the process command before terminating this lesson's process tree.
        try:
            import psutil

            process = psutil.Process(old["pid"])
            if (
                str(ROOT / "app.py") in process.cmdline()
                and abs(process.create_time() - old["created"]) < 1
            ):
                children = process.children(recursive=True)
                for child in reversed(children):
                    try:
                        child.terminate()
                    except psutil.NoSuchProcess:
                        pass
                process.terminate()
                _, alive = psutil.wait_procs(children + [process], timeout=5)
                for remaining in alive:
                    remaining.kill()
        except ImportError:
            print(
                "Restart wymaga psutil. Zamknij poprzednią instancję lub zainstaluj requirements.txt."
            )
            return 1
        except psutil.NoSuchProcess:
            pass
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
            with urllib.request.urlopen(
                "http://127.0.0.1:8031/api/course", timeout=1
            ):
                break
        except OSError:
            time.sleep(0.25)
    else:
        process.terminate()
        print("Serwer nie odpowiedział. Sprawdź .runtime/server.log.")
        return 1
    print("Lekcja 31: http://127.0.0.1:8031/")
    print("Asyncio Studio — 20 zadań, analiza kodu i rzeczywiste wyniki.")
    if not args.no_browser:
        webbrowser.open("http://127.0.0.1:8031/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
