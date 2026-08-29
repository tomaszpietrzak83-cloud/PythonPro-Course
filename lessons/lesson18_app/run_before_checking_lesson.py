"""Create a lesson-local virtual environment and install dependencies."""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
VENV_DIR = ROOT_DIR / ".venv"
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"


def get_venv_python() -> Path:
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run(command):
    printable_command = " ".join(str(part) for part in command)
    print(f"\n$ {printable_command}")
    subprocess.check_call([str(part) for part in command], cwd=ROOT_DIR)


def ensure_requirements_file() -> None:
    if not REQUIREMENTS_FILE.exists():
        raise SystemExit(f"Missing requirements file: {REQUIREMENTS_FILE.name}")


def ensure_virtual_environment() -> None:
    if VENV_DIR.exists():
        print(f"Using existing virtual environment: {VENV_DIR}")
        return

    run([sys.executable, "-m", "venv", VENV_DIR])


def install_requirements() -> None:
    python_path = get_venv_python()
    if not python_path.exists():
        raise SystemExit(
            "The virtual environment exists, but its Python executable was "
            f"not found at: {python_path}"
        )

    run([python_path, "-m", "pip", "install", "--upgrade", "pip"])
    run([python_path, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])


def print_next_steps() -> None:
    print("\nSetup complete.")
    print("\nActivate the lesson environment with:")
    if sys.platform == "win32":
        print(r".venv\Scripts\activate")
    else:
        print("source .venv/bin/activate")


def main() -> None:
    ensure_requirements_file()
    ensure_virtual_environment()
    install_requirements()
    print_next_steps()


if __name__ == "__main__":
    main()
