"""# TASK 20 - Zaloguj się i pobierz chroniony profil.

Ustaw zmienne środowiskowe DJANGO_USERNAME i DJANGO_PASSWORD przed uruchomieniem.
Uruchom serwer Django z lekcji 26 w osobnym terminalu.
"""

import os

import requests

# TASK 20
BASE_URL = os.getenv("DJANGO_BASE_URL", "http://127.0.0.1:8000")
USERNAME = os.getenv("DJANGO_USERNAME")
PASSWORD = os.getenv("DJANGO_PASSWORD")


def main():
    if not USERNAME or not PASSWORD:
        raise SystemExit("Ustaw zmienne DJANGO_USERNAME i DJANGO_PASSWORD.")

    login_response = requests.post(
        f"{BASE_URL}/auth/jwt/create/",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=10,
    )
    login_response.raise_for_status()
    access_token = login_response.json()["access"]

    profile_response = requests.get(
        f"{BASE_URL}/user/",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    profile_response.raise_for_status()
    print(profile_response.json())


if __name__ == "__main__":
    main()
