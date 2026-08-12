"""
Bootstrap script - Syncs requirements.txt with installed packages
and validates .gitignore configuration.
Run at the beginning of your program.
"""

import subprocess
import sys
from pathlib import Path


def get_installed_packages():
    """Returns a dict of installed packages and their versions."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format", "json"],
        capture_output=True,
        text=True,
    )
    packages = {}
    try:
        import json

        for pkg in json.loads(result.stdout):
            packages[pkg["name"].lower()] = pkg["version"]
    except:
        pass
    return packages


def parse_requirements(file_path="requirements.txt"):
    """Parses requirements.txt and returns a dict of packages."""
    requirements = {}
    if not Path(file_path).exists():
        return requirements

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # Handles: package, package==1.0, package>=1.0, etc.
                pkg_name = (
                    line
                    .split("==")[0]
                    .split(">=")[0]
                    .split("<=")[0]
                    .split(">")[0]
                    .split("<")[0]
                    .strip()
                )
                requirements[pkg_name.lower()] = line
    return requirements


def parse_gitignore(file_path=".gitignore"):
    """Parses .gitignore and returns a list of patterns."""
    patterns = []
    if not Path(file_path).exists():
        return patterns

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def check_gitignore():
    """Validates that .gitignore contains essential Python patterns."""
    essential_patterns = [
        "venv/",
        "__pycache__/",
        "*.pyc",
        ".env",
        "*.db",
        ".vscode/",
    ]

    if not Path(".gitignore").exists():
        print("📄 .gitignore not found. Skipping validation.")
        return

    existing_patterns = parse_gitignore()
    missing_patterns = []

    for pattern in essential_patterns:
        if pattern not in existing_patterns:
            missing_patterns.append(pattern)

    if missing_patterns:
        print(
            f"⚠️  Found {len(missing_patterns)} missing patterns in .gitignore:"
        )
        with open(".gitignore", "a") as f:
            for pattern in missing_patterns:
                f.write(pattern + "\n")
                print(f"  ✅ Added: {pattern}")
        print("📝 .gitignore updated!\n")
    else:
        print("✅ .gitignore contains all essential patterns\n")


def update_requirements():
    """Checks differences between installed packages and requirements.txt."""
    installed = get_installed_packages()
    required = parse_requirements()

    # Skip if requirements.txt doesn't exist
    if not Path("requirements.txt").exists():
        print("📄 requirements.txt not found. Skipping.")
        return

    # Check if all installed packages are in requirements.txt
    new_packages = []
    for pkg_name, version in installed.items():
        if pkg_name not in required and pkg_name not in [
            "pip",
            "setuptools",
            "wheel",
        ]:
            new_packages.append(f"{pkg_name}=={version}")

    if new_packages:
        print(f"✨ Found {len(new_packages)} new packages!")
        with open("requirements.txt", "a") as f:
            for pkg in new_packages:
                f.write(pkg + "\n")
                print(f"  ✅ Added: {pkg}")
        print("📝 requirements.txt updated!\n")
    else:
        print("✅ requirements.txt is in sync with installed packages\n")


def bootstrap():
    """Main bootstrap function."""
    print("🚀 Bootstrap starting...\n")
    check_gitignore()
    update_requirements()


if __name__ == "__main__":
    bootstrap()
