import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"


def get_packages():
    package_text = input("Package name to uninstall: ").strip()

    if not package_text:
        print("No package name provided.")
        sys.exit(1)

    return package_text.split()


def uninstall_packages(packages):
    if not VENV_PYTHON.exists():
        print(f"Virtual environment Python was not found: {VENV_PYTHON}")
        print("Create the virtual environment first with:")
        print("python -m venv .venv")
        sys.exit(1)

    print(f"Uninstalling from: {VENV_PYTHON}", flush=True)
    print(f"Package(s): {', '.join(packages)}", flush=True)
    print(flush=True)

    command = [str(VENV_PYTHON), "-m", "pip", "uninstall", "-y", *packages]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print()
        print("Uninstallation failed.")
        sys.exit(exc.returncode)

    print()
    print("Uninstallation finished successfully.")


def main():
    packages = get_packages()
    uninstall_packages(packages)


if __name__ == "__main__":
    main()
