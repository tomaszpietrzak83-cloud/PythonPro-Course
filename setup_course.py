"""Create or update the single course environment."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    python = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        subprocess.run([sys.executable, "-m", "venv", str(ROOT / ".venv")], check=True)
    uv = shutil.which("uv")
    requirements = ROOT / "requirements.txt"
    lock = ROOT / "requirements-lock.txt"
    if uv:
        command = [uv, "pip", "install", "--python", str(python.relative_to(ROOT)), "--cache-dir", ".uv-cache", "-r", requirements.name]
        check = [uv, "pip", "check", "--python", str(python.relative_to(ROOT)), "--cache-dir", ".uv-cache"]
    else:
        command = [str(python), "-m", "pip", "install", "-r", requirements.name]
        check = [str(python), "-m", "pip", "check"]
    # Constraints preserve tested versions without installing Windows-only
    # distributions on other systems.
    if lock.exists():
        command.extend(["-c", lock.name])
    subprocess.run(command, cwd=ROOT, check=True)
    subprocess.run(check, cwd=ROOT, check=True)
    print(f"Gotowe. Interpreter kursu: {python}")


if __name__ == "__main__":
    main()
