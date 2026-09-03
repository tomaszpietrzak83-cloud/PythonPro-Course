import os
import socket
import subprocess
import sys
import time
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DOCKER_CONTAINER_NAME = "redis-cache"
DOCKER_PORT = 6379
TIME_SLEEP = 0.7


DOCKER_BIN_DIRS = [
    Path.home()
    / "AppData"
    / "Local"
    / "Programs"
    / "DockerDesktop"
    / "resources"
    / "bin",
    Path("C:/Program Files/Docker/Docker/resources/bin"),
]

DOCKER_DESKTOP_PATHS = [
    Path.home()
    / "AppData"
    / "Local"
    / "Programs"
    / "DockerDesktop"
    / "Docker Desktop.exe",
    Path("C:/Program Files/Docker/Docker/Docker Desktop.exe"),
]


def print_message(message):
    print(message)
    time.sleep(TIME_SLEEP)


def run_powershell(command):
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            command,
        ],
        text=True,
    )

    if result.returncode != 0:
        sys.exit(result.returncode)


def find_docker_bin_dir():
    for docker_bin_dir in DOCKER_BIN_DIRS:
        if (docker_bin_dir / "docker.exe").exists():
            return docker_bin_dir

    print_message("docker.exe was not found.")
    print_message("Check whether Docker Desktop is installed.")
    sys.exit(1)


def start_docker_desktop():
    for docker_desktop_path in DOCKER_DESKTOP_PATHS:
        if docker_desktop_path.exists():
            print_message(
                "Starting Docker Desktop if it is not already running..."
            )
            command = f'Start-Process -FilePath "{docker_desktop_path}" -WindowStyle Hidden'
            run_powershell(command)
            return

    print_message(
        "Docker Desktop app was not found, but docker.exe may still work."
    )


def wait_for_redis(timeout_seconds=30):
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex(("127.0.0.1", DOCKER_PORT)) == 0:
                return True

        time.sleep(1)

    return False


def start_redis_container():
    docker_bin_dir = find_docker_bin_dir()
    start_docker_desktop()

    path_prefix = str(docker_bin_dir)
    command = (
        f'$env:Path = "{path_prefix};$env:Path"; '
        f"docker container inspect {DOCKER_CONTAINER_NAME} *> $null; "
        "if ($LASTEXITCODE -eq 0) { "
        f"docker start {DOCKER_CONTAINER_NAME} "
        "} else { "
        f"docker run --name {DOCKER_CONTAINER_NAME} -p {DOCKER_PORT}:{DOCKER_PORT} -d redis "
        "}"
    )

    print_message("Starting Redis container with PowerShell...")
    run_powershell(command)

    if not wait_for_redis():
        print_message("Redis did not start on 127.0.0.1:6379.")
        print_message("Open Docker Desktop and run this script again.")
        sys.exit(1)

    print_message("Redis is running on 127.0.0.1:6379.")


def test_django_cache():
    os.chdir(PROJECT_DIR)
    sys.path.insert(0, str(PROJECT_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l27_pro_3.settings")

    import django

    django.setup()

    from django.core.cache import cache
    from django.test import Client

    cache.set("redis_helper_test_key", "works", timeout=30)
    cache_value = cache.get("redis_helper_test_key")

    if cache_value != "works":
        print_message("Django could not read the test value from Redis.")
        sys.exit(1)

    response = Client(HTTP_HOST="127.0.0.1").get(
        "/api/task10/products/",
        HTTP_ACCEPT="text/html",
    )

    print_message(f"Django cache test value: {cache_value}")
    print_message(f"Products endpoint status: {response.status_code}")


def main():
    start_redis_container()
    test_django_cache()
    print_message("Redis cache is ready for testing.")


if __name__ == "__main__":
    main()
