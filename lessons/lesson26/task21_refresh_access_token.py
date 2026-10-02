"""# TASK 21 - Odśwież access token po odpowiedzi 401.

Ustaw DJANGO_USERNAME i DJANGO_PASSWORD, a serwer uruchom osobno.
"""

import os

import requests

# TASK 21
BASE_URL = os.getenv("DJANGO_BASE_URL", "http://127.0.0.1:8000")
USERNAME = os.getenv("DJANGO_USERNAME")
PASSWORD = os.getenv("DJANGO_PASSWORD")
ACCESS_TOKEN = os.getenv("DJANGO_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("DJANGO_REFRESH_TOKEN")


def login(session):
    response = session.post(
        f"{BASE_URL}/auth/jwt/create/",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def get_profile(session, access_token):
    return session.get(
        f"{BASE_URL}/user/",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )


def refresh_access_token(session, refresh_token):
    response = session.post(
        f"{BASE_URL}/auth/jwt/refresh/",
        json={"refresh": refresh_token},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["access"]


def main():
    with requests.Session() as session:
        if ACCESS_TOKEN and REFRESH_TOKEN:
            access_token = ACCESS_TOKEN
            refresh_token = REFRESH_TOKEN
        else:
            if not USERNAME or not PASSWORD:
                raise SystemExit(
                    "Ustaw DJANGO_ACCESS_TOKEN i DJANGO_REFRESH_TOKEN albo "
                    "DJANGO_USERNAME i DJANGO_PASSWORD."
                )
            tokens = login(session)
            access_token = tokens["access"]
            refresh_token = tokens["refresh"]

        response = get_profile(session, access_token)

        if response.status_code == 401:
            access_token = refresh_access_token(session, refresh_token)
            response = get_profile(session, access_token)

        response.raise_for_status()
        print(response.json())


if __name__ == "__main__":
    main()
