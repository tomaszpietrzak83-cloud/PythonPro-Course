import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l25_pro.settings")
django.setup()

# TASK 09
from new_app.models import Author, Book

# TASK 09
DATA = [
    {
        "author": "George Orwell",
        "books": [
            ("Animal Farm", "1945"),
            ("Nineteen Eighty-Four", "1949"),
        ],
    },
    {
        "author": "J.K. Rowling",
        "books": [
            ("Harry Potter and the Philosopher's Stone", "1997"),
            ("Harry Potter and the Chamber of Secrets", "1998"),
        ],
    },
    {
        "author": "Frank Herbert",
        "books": [
            ("Dune", "1965"),
            ("Dune Messiah", "1969"),
        ],
    },
]


def run():
    # TASK 09
    for item in DATA:
        author, _ = Author.objects.get_or_create(name=item["author"])

        for title, publication_year in item["books"]:
            Book.objects.update_or_create(
                title=title,
                defaults={
                    "publication_year": publication_year,
                    "author": author,
                },
            )

    print("Authors and books seeded.")


if __name__ == "__main__":
    run()
