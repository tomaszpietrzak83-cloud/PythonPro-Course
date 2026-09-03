import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"


def get_packages():
    package_text = input("Package name to install: ").strip()

    if not package_text:
        print("No package name provided.")
        sys.exit(1)

    return package_text.split()


def install_packages(packages):
    if not VENV_PYTHON.exists():
        print(f"Virtual environment Python was not found: {VENV_PYTHON}")
        print("Create the virtual environment first with:")
        print("python -m venv .venv")
        sys.exit(1)

    print(f"Installing into: {VENV_PYTHON}", flush=True)
    print(f"Package(s): {', '.join(packages)}", flush=True)
    print(flush=True)

    command = [str(VENV_PYTHON), "-m", "pip", "install", *packages]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print()
        print("Installation failed.")
        sys.exit(exc.returncode)

    print()
    print("Installation finished successfully.")


def main():
    packages = get_packages()
    install_packages(packages)


if __name__ == "__main__":
    main()
