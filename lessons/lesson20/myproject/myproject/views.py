from django.http import HttpResponse
from django.urls import reverse

from notes.models import Note
from products.models import Category


def home(request):
    links = [
        ("Informacje", reverse("products:info")),
        ("Regulamin", reverse("products:rules")),
        ("Powitanie uzytkownika", reverse("products:user_greeting", args=["kursant"])),
        ("Lista produktow", reverse("products:product_list")),
        ("Dodaj produkt", reverse("products:product_creation")),
        ("Lista notatek", reverse("notes:notes_list")),
        ("Panel admina", reverse("admin:index")),
    ]

    html_links = "".join(
        f'<li><a href="{url}">{title}</a></li>' for title, url in links
    )

    category_links = "".join(
        f'<li><a href="{reverse("products:category_view", args=[category.id])}">'
        f"Kategoria: {category.name}</a></li>"
        for category in Category.objects.all().order_by("id")
    )

    note_links = "".join(
        f'<li><a href="{reverse("notes:note_detail", args=[note.id])}">'
        f"Notatka: {note.title}</a></li>"
        for note in Note.objects.all().order_by("id")
    )

    return HttpResponse(
        f"""
        <!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <title>Lekcja 20 - widoki</title>
        </head>
        <body>
            <h1>Lekcja 20 - wszystkie widoki</h1>
            <p>Prosta strona startowa z linkami do pozostalych widokow.</p>

            <h2>Glowne linki</h2>
            <ul>{html_links}</ul>

            <h2>Kategorie</h2>
            <ul>{category_links or "<li>Brak kategorii w bazie.</li>"}</ul>

            <h2>Notatki</h2>
            <ul>{note_links or "<li>Brak notatek w bazie.</li>"}</ul>
        </body>
        </html>
        """
    )
