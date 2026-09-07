import os
import sys
from getpass import getpass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l28_pro.settings")


def ask_value(label, default=""):
    prompt = f"{label} [{default}]: " if default else f"{label}: "
    value = input(prompt).strip()
    return value or default


def ask_password():
    while True:
        password = getpass("Password: ")
        repeated_password = getpass("Repeat password: ")

        if password != repeated_password:
            print("Passwords do not match. Try again.")
            continue

        if not password:
            print("Password cannot be empty. Try again.")
            continue

        return password


def main():
    import django

    try:
        django.setup()
    except ModuleNotFoundError as error:
        if error.name == "dotenv":
            print("Missing dependency: python-dotenv")
            print("Install it with: pip install python-dotenv")
            raise SystemExit(1) from error
        raise
    except RuntimeError as error:
        print(f"Django settings error: {error}")
        raise SystemExit(1) from error

    from django.contrib.auth import get_user_model
    from django.contrib.auth.password_validation import validate_password
    from django.core.exceptions import ValidationError

    User = get_user_model()

    username = ask_value("Username", "admin")
    email = ask_value("Email", "admin@example.com")

    existing_user = User.objects.filter(username=username).first()
    if existing_user:
        if existing_user.is_superuser and existing_user.is_staff:
            print(f"Superuser '{username}' already exists.")
            return

        answer = ask_value(
            f"User '{username}' exists but is not a superuser. Promote? y/N",
            "N",
        )
        if answer.lower() != "y":
            print("No changes made.")
            return

        existing_user.is_staff = True
        existing_user.is_superuser = True
        existing_user.save(update_fields=["is_staff", "is_superuser"])
        print(f"User '{username}' was promoted to superuser.")
        return

    while True:
        password = ask_password()
        try:
            validate_password(password)
        except ValidationError as error:
            print("Password validation failed:")
            for message in error.messages:
                print(f"- {message}")

            answer = ask_value("Try another password? Y/n", "Y")
            if answer.lower() == "n":
                return
            continue

        break

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print(f"Superuser '{username}' was created.")


if __name__ == "__main__":
    main()
