import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANAGE_PY = BASE_DIR / "manage.py"
SERVER_ADDRESS = "127.0.0.1:8000"


def run_manage(*args, stop_on_error=True):
    command = [sys.executable, str(MANAGE_PY), *args]
    print(f"\n>>> {' '.join(command)}")
    result = subprocess.run(command, cwd=BASE_DIR)
    if stop_on_error and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def has_model_changes():
    return run_manage("makemigrations", "--check", "--dry-run", stop_on_error=False) != 0


def main():
    if has_model_changes():
        run_manage("makemigrations")
        run_manage("migrate")
    run_manage("runserver", SERVER_ADDRESS, "--noreload")


if __name__ == "__main__":
    main()
