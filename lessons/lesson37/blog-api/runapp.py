import subprocess
import sys
from pathlib import Path
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

PROJECT_DIR = Path(__file__).resolve().parent
COMPOSE = ["docker", "compose"]
POSTS_URL = "http://localhost/api/posts/"


def main():
    try:
        subprocess.run(
            [*COMPOSE, "up", "--build", "--wait", "--wait-timeout", "120"],
            cwd=PROJECT_DIR,
            check=True,
        )
    except FileNotFoundError:
        print("Nie znaleziono polecenia docker.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(
            "Docker Compose nie uruchomił projektu. Szczegóły są powyżej.",
            file=sys.stderr,
        )
        return error.returncode

    for attempt in range(10):
        try:
            with urlopen(POSTS_URL, timeout=2) as response:
                print(f"Blog API odpowiada: HTTP {response.status} {POSTS_URL}")
            return 0
        except (URLError, TimeoutError) as error:
            last_error = error
            if attempt < 9:
                sleep(2)

    print(
        f"Endpoint {POSTS_URL} nie odpowiada poprawnie: {last_error}",
        file=sys.stderr,
    )
    subprocess.run([*COMPOSE, "ps"], cwd=PROJECT_DIR)
    return 1


if __name__ == "__main__":
    sys.exit(main())
