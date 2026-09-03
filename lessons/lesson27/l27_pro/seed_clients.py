import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l27_pro.settings")

import django

django.setup()

from random import randint

from faker import Faker
from myapp.models import Client

CLIENT_COUNT = 21


def build_client_data(number):
    fake = Faker("en_US")
    Faker.seed(randint(1, 1_000_000))

    clients = []

    for _ in range(number):
        clients.append({
            "name": fake.name(),
            "email": fake.unique.email(),
            "city": fake.city(),
            "bank": f"{fake.company()} Bank",
        })

    return clients


def save_client(client_data):
    client, created = Client.objects.update_or_create(
        email=client_data["email"],
        defaults={
            "name": client_data["name"],
            "city": client_data["city"],
            "bank": client_data["bank"],
        },
    )

    if created:
        print(f"Created: {client.name}")
    else:
        print(f"Updated: {client.name}")

    return created


def print_summary(created_count, updated_count):
    total_count = Client.objects.count()

    print()
    print("Client seeding finished.")
    print(f"Created clients: {created_count}")
    print(f"Updated clients: {updated_count}")
    print(f"Total clients in database: {total_count}")


def seed_clients():
    created_count = 0
    updated_count = 0

    if CLIENT_COUNT > Client.objects.count():
        for client_data in build_client_data(
            CLIENT_COUNT - Client.objects.count()
        ):
            created = save_client(client_data)

            if created:
                created_count += 1
            else:
                updated_count += 1

        print_summary(created_count, updated_count)

    else:
        for client_data in build_client_data(CLIENT_COUNT):
            created = save_client(client_data)

            if created:
                created_count += 1
            else:
                updated_count += 1

        print_summary(created_count, updated_count)


if __name__ == "__main__":
    seed_clients()
