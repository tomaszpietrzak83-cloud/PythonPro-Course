import os
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l27_pro.settings")

import django
from django.core.management import call_command

django.setup()

from myapp.models import Product

PRODUCTS = [
    {
        "name": "Laptop",
        "price": "3499.99",
        "short_description": "Powerful laptop for work and study.",
    },
    {
        "name": "Smartphone",
        "price": "2199.00",
        "short_description": "Fast phone with a sharp display.",
    },
    {
        "name": "Wireless Mouse",
        "price": "89.99",
        "short_description": "Comfortable mouse for daily use.",
    },
    {
        "name": "Mechanical Keyboard",
        "price": "299.99",
        "short_description": "Durable keyboard with tactile switches.",
    },
    {
        "name": "Monitor",
        "price": "799.00",
        "short_description": "Large screen for coding and gaming.",
    },
    {
        "name": "USB-C Hub",
        "price": "149.99",
        "short_description": "Extra ports for your laptop.",
    },
    {
        "name": "Bluetooth Speaker",
        "price": "199.99",
        "short_description": "Portable speaker with clear sound.",
    },
    {
        "name": "Smartwatch",
        "price": "699.99",
        "short_description": "Watch for notifications and fitness.",
    },
    {
        "name": "Desk Lamp",
        "price": "119.99",
        "short_description": "Adjustable lamp for focused work.",
    },
    {"name": "Headphones", "price": "349.99"},
    {"name": "Tablet", "price": "1299.00"},
    {"name": "External Drive", "price": "269.99"},
    {"name": "Webcam", "price": "229.99"},
    {"name": "Microphone", "price": "319.99"},
    {"name": "Office Chair", "price": "549.00"},
    {"name": "Backpack", "price": "179.99"},
    {"name": "Power Bank", "price": "139.99"},
    {"name": "Router", "price": "249.99"},
    {"name": "Graphics Tablet", "price": "399.99"},
    {"name": "Gaming Controller", "price": "259.99"},
]


def seed_products():
    # if forget migrations
    call_command("migrate", interactive=False, verbosity=0)
    created_count = 0
    updated_count = 0

    for product_data in PRODUCTS:
        defaults = {
            "price": Decimal(product_data["price"]),
        }

        # Let the model use its default value when no short description is provided.
        if "short_description" in product_data:
            defaults["short_description"] = product_data["short_description"]

        product, created = Product.objects.update_or_create(
            name=product_data["name"],
            defaults=defaults,
        )

        if created:
            created_count += 1
            print(f"Created: {product.name}")
        else:
            updated_count += 1
            print(f"Updated: {product.name}")

    total_count = Product.objects.count()
    described_count = Product.objects.exclude(short_description="empty").count()

    print()
    print("Seeding finished.")
    print(f"Created products: {created_count}")
    print(f"Updated products: {updated_count}")
    print(f"Total products in database: {total_count}")
    print(f"Products with short description: {described_count}")


if __name__ == "__main__":
    seed_products()
