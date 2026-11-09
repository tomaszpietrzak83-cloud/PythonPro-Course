import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


def main():
    try:
        result = subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "backend",
                "python",
                "manage.py",
                "createsuperuser",
            ],
            cwd=PROJECT_DIR,
        )
    except FileNotFoundError:
        print("Nie znaleziono polecenia docker.", file=sys.stderr)
        return 1

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
