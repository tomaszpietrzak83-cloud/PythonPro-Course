"""Bootstrap helpers for the Lesson 19 Django project.

This script keeps a few project files in a sane state:
- .gitignore contains essential Python/Django patterns
- requirements.txt can be rebuilt from the active virtualenv
- .env.example exists as a safe template
- .env is created once if missing
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
GITIGNORE_PATH = ROOT_DIR / ".gitignore"
REQUIREMENTS_PATH = ROOT_DIR / "requirements.txt"
ENV_PATH = ROOT_DIR / ".env"
ENV_EXAMPLE_PATH = ROOT_DIR / ".env.example"

REQUIRED_GITIGNORE_PATTERNS = [
    ".venv/",
    "venv/",
    "env/",
    "__pycache__/",
    "*.py[cod]",
    ".env",
    ".env.*",
    "!.env.example",
    "*.sqlite3",
    "*.db",
    ".vscode/",
    ".idea/",
]

ESSENTIAL_REQUIREMENTS = [
    "Django==5.2.15",
    "psycopg2-binary==2.9.12",
    "python-dotenv==1.2.2",
]

ENV_TEMPLATE = """DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_TIME_ZONE=UTC
POSTGRES_DB=mojprojekt19
POSTGRES_USER=postgres
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
"""


def read_nonempty_lines(path: Path):
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def ensure_gitignore():
    existing = read_nonempty_lines(GITIGNORE_PATH)
    missing = [
        pattern
        for pattern in REQUIRED_GITIGNORE_PATTERNS
        if pattern not in existing
    ]

    if not GITIGNORE_PATH.exists():
        GITIGNORE_PATH.write_text("", encoding="utf-8")

    if not missing:
        print("OK .gitignore contains the required patterns")
        return

    existing_text = GITIGNORE_PATH.read_text(encoding="utf-8")
    with GITIGNORE_PATH.open("a", encoding="utf-8") as file:
        if existing_text and not existing_text.endswith("\n"):
            file.write("\n")
        for pattern in missing:
            file.write(pattern + "\n")

    print(f"Updated .gitignore with {len(missing)} missing patterns")


def rebuild_requirements_from_pip_freeze():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True,
    )

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    missing_essentials = [
        requirement
        for requirement in ESSENTIAL_REQUIREMENTS
        if not any(
            line.lower().startswith(requirement.split("==")[0].lower())
            for line in lines
        )
    ]

    final_lines = lines + missing_essentials
    REQUIREMENTS_PATH.write_text(
        "\n".join(final_lines) + "\n",
        encoding="utf-8",
    )

    print(
        "Rebuilt requirements.txt from the active environment "
        f"with {len(final_lines)} entries"
    )


def ensure_env_files():
    if not ENV_EXAMPLE_PATH.exists():
        ENV_EXAMPLE_PATH.write_text(ENV_TEMPLATE, encoding="utf-8")
        print("Created .env.example")
    else:
        print("OK .env.example already exists")

    if not ENV_PATH.exists():
        ENV_PATH.write_text(ENV_TEMPLATE, encoding="utf-8")
        print("Created .env - fill in POSTGRES_PASSWORD and SECRET_KEY")
    else:
        print("OK .env already exists")


def bootstrap():
    print("Starting bootstrap checks...\n")
    ensure_gitignore()
    rebuild_requirements_from_pip_freeze()
    ensure_env_files()
    print("\nBootstrap finished.")


if __name__ == "__main__":
    bootstrap()
