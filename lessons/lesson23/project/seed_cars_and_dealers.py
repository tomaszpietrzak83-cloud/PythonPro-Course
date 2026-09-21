"""Create sample dealers and cars for the Lesson 23 Django project.

Run from the ``project`` folder:
    python seed_cars_and_dealers.py
"""

import os

import django
from django.core.files.base import ContentFile

# Django models need the settings to be loaded before they can be imported.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from cars.models import Car, Dealer

DEALERS = [
    ("AutoMax Warszawa", "ul. Puławska 101, 02-595 Warszawa"),
    ("Kraków Motors", "ul. Zakopiańska 62, 30-418 Kraków"),
    ("Wrocław Auto Centrum", "ul. Legnicka 57, 54-203 Wrocław"),
    ("Poznań Car House", "ul. Głogowska 190, 60-116 Poznań"),
    ("Gdańsk Premium Cars", "ul. Grunwaldzka 472, 80-309 Gdańsk"),
]


CARS = [
    (
        "Toyota",
        "Corolla",
        2021,
        "76900.00",
        "Ekonomiczny sedan, pierwszy właściciel.",
        0,
        True,
    ),
    (
        "Toyota",
        "RAV4",
        2022,
        "149900.00",
        "Hybrydowy SUV z kamerą cofania.",
        0,
        True,
    ),
    (
        "Skoda",
        "Octavia",
        2020,
        "82900.00",
        "Przestronne kombi z historią serwisową.",
        0,
        True,
    ),
    (
        "Volkswagen",
        "Golf",
        2019,
        "68900.00",
        "Kompakt w bardzo dobrym stanie.",
        0,
        False,
    ),
    (
        "BMW",
        "320i",
        2021,
        "159900.00",
        "Sedan z automatyczną skrzynią biegów.",
        1,
        True,
    ),
    ("BMW", "X3", 2020, "189900.00", "SUV z napędem xDrive.", 1, True),
    (
        "Audi",
        "A4",
        2021,
        "154900.00",
        "Komfortowy sedan z pełnym wyposażeniem.",
        1,
        True,
    ),
    (
        "Mercedes-Benz",
        "GLA 200",
        2022,
        "179900.00",
        "Miejski crossover z pakietem premium.",
        1,
        False,
    ),
    (
        "Ford",
        "Focus",
        2018,
        "49900.00",
        "Hatchback, regularnie serwisowany.",
        2,
        True,
    ),
    (
        "Ford",
        "Kuga",
        2021,
        "124900.00",
        "Rodzinny SUV z bogatym wyposażeniem.",
        2,
        True,
    ),
    (
        "Mazda",
        "CX-5",
        2020,
        "119900.00",
        "SUV z silnikiem benzynowym 2.0.",
        2,
        True,
    ),
    ("Hyundai", "i30", 2019, "62900.00", "Praktyczne auto miejskie.", 2, False),
    (
        "Kia",
        "Sportage",
        2021,
        "129900.00",
        "SUV z gwarancją producenta.",
        3,
        True,
    ),
    (
        "Kia",
        "Ceed",
        2020,
        "74900.00",
        "Kombi z nawigacją i kamerą cofania.",
        3,
        True,
    ),
    (
        "Renault",
        "Megane",
        2019,
        "57900.00",
        "Hatchback w wersji Intens.",
        3,
        True,
    ),
    (
        "Peugeot",
        "3008",
        2021,
        "132900.00",
        "Nowoczesny SUV z automatem.",
        3,
        False,
    ),
    (
        "Volvo",
        "XC60",
        2020,
        "199900.00",
        "Bezpieczny SUV z napędem AWD.",
        4,
        True,
    ),
    ("Volvo", "V60", 2019, "139900.00", "Kombi klasy premium.", 4, True),
    (
        "Lexus",
        "NX 300h",
        2021,
        "184900.00",
        "Hybrydowy SUV z pełną historią.",
        4,
        True,
    ),
    (
        "Nissan",
        "Qashqai",
        2020,
        "96900.00",
        "Crossover z panoramicznym dachem.",
        4,
        False,
    ),
]


def placeholder_photo(brand, model):
    """Return a small SVG saved by ImageField as a local placeholder photo."""
    label = f"{brand} {model}".replace("&", "and")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450">
    <rect width="100%" height="100%" fill="#1f2937"/>
    <text x="50%" y="45%" text-anchor="middle" fill="white"
          font-family="Arial" font-size="44">{label}</text>
    <text x="50%" y="58%" text-anchor="middle" fill="#93c5fd"
          font-family="Arial" font-size="24">Sample car photo</text>
    </svg>"""
    return ContentFile(svg.encode("utf-8"))


def run():
    dealers = []
    for name, address in DEALERS:
        dealer, _ = Dealer.objects.update_or_create(
            name=name, defaults={"address": address}
        )
        dealers.append(dealer)

    created_count = 0
    for (
        brand,
        model,
        year,
        price,
        description,
        dealer_index,
        is_available,
    ) in CARS:
        car, created = Car.objects.get_or_create(
            brand=brand,
            model=model,
            year=year,
            defaults={
                "price": price,
                "description": description,
                "dealer": dealers[dealer_index],
                "is_available": is_available,
            },
        )

        # A photo is required by the model. Create it only for new or incomplete data.
        if created or not car.photo:
            filename = (
                f"{brand.lower()}-{model.lower().replace(' ', '-')}-{year}.svg"
            )
            car.photo.save(
                filename, placeholder_photo(brand, model), save=False
            )

        car.price = price
        car.description = description
        car.dealer = dealers[dealer_index]
        car.is_available = is_available
        car.save()
        created_count += created

    print(f"Seed complete: {len(dealers)} dealers and {len(CARS)} cars.")
    print(f"New cars created during this run: {created_count}.")


if __name__ == "__main__":
    run()
