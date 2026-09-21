import subprocess
import sys
from pathlib import Path

LESSON_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LESSON_DIR / "my_project"
MANAGE_PY = PROJECT_DIR / "manage.py"


def find_python():
    """Find the course or standalone lesson virtual environment."""
    course_dir = LESSON_DIR.parents[1]
    executable = "python.exe" if sys.platform == "win32" else "python"
    script_dir = "Scripts" if sys.platform == "win32" else "bin"
    candidates = [
        course_dir / ".venv" / script_dir / executable,
        LESSON_DIR / ".venv" / script_dir / executable,
        Path(sys.executable),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit("A Python executable could not be found.")


def main():
    command = [
        str(find_python()),
        str(MANAGE_PY),
        "createsuperuser",
        *sys.argv[1:],
    ]
    print(f"\n>>> {' '.join(command)}")
    result = subprocess.run(command, cwd=PROJECT_DIR)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
