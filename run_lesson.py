"""Run any lesson script with the shared interpreter and correct directory."""
import argparse
from pathlib import Path
import subprocess

from course_runtime import PYTHON, ROOT


def main():
    parser = argparse.ArgumentParser(description="Uruchom plik lekcji we wspólnym .venv.")
    parser.add_argument("script", help="Ścieżka do pliku .py, względem głównego katalogu kursu.")
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    script = (ROOT / args.script).resolve()
    if not script.is_relative_to(ROOT / "lessons") or script.suffix != ".py" or not script.is_file():
        parser.error("Podaj istniejący plik .py w katalogu lessons.")
    if not PYTHON.exists():
        parser.error("Brak .venv. Uruchom python setup_course.py.")
    try:
        return subprocess.call([str(PYTHON), str(script), *args.arguments], cwd=script.parent)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
