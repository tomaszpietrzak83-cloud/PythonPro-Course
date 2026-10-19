"""Shared interpreter and Django launcher for the course."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def use_course_python(script):
    if not PYTHON.exists():
        raise SystemExit("Brak wspólnego .venv. Uruchom: python setup_course.py")
    if Path(sys.executable).resolve() != PYTHON.resolve():
        raise SystemExit(subprocess.call([str(PYTHON), str(script), *sys.argv[1:]]))


def run_django(script, default_port=8000):
    use_course_python(script)
    parser = argparse.ArgumentParser(description="Uruchom projekt we wspólnym .venv kursu.")
    parser.add_argument("--check", action="store_true", help="Sprawdź konfigurację bez uruchamiania i migracji.")
    parser.add_argument("--no-migrate", action="store_true")
    parser.add_argument("--port", type=int, default=default_port)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port musi mieścić się w zakresie 1–65535.")
    base = Path(script).resolve().parent

    def manage(*commands):
        subprocess.run([str(PYTHON), str(base / "manage.py"), *commands], cwd=base, check=True)

    try:
        manage("check")
        if args.check:
            return
        # Apply existing migrations even when model definitions haven't changed.
        if not args.no_migrate:
            manage("migrate", "--noinput")
        manage("runserver", f"127.0.0.1:{args.port}", "--noreload")
    except KeyboardInterrupt:
        return
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error
