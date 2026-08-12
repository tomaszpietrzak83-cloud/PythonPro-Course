# --- TASK 08 ---
from .models import Category


def init_categories():
    categories = [
        {"name": "Electronics"},
        {"name": "Clothing"},
        {"name": "Home & Kitchen"},
        {"name": "Books"},
        {"name": "Toys & Games"},
        {"name": "Sports & Outdoors"},
        {"name": "Health & Personal Care"},
        {"name": "Automotive"},
        {"name": "Beauty"},
        {"name": "Grocery"},
    ]

    for category_data in categories:
        category, created = Category.objects.get_or_create(
            name=category_data["name"]
        )

        if created:
            print(f"Added: {category.name}")
        else:
            print(f"Already exists: {category.name}")
