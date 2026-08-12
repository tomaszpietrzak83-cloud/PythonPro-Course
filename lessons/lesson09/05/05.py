# Importuje modul csv, aby zapisac dane do pliku CSV.
import csv

# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

# Tworze liste slownikow z przykladowymi produktami i ich cenami.
produkty = [
    # Dodaje pierwszy produkt do listy.
    {"nazwa": "Mleko", "cena": 3.50},
    # Dodaje drugi produkt do listy.
    {"nazwa": "Chleb", "cena": 4.20},
]

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku produkty.csv w tym samym folderze co skrypt.
sciezka_pliku = folder_skryptu / "produkty.csv"

# Otwieram plik CSV do zapisu i ustawiam newline="", aby nie tworzyc pustych wierszy.
with sciezka_pliku.open("w", encoding="utf-8", newline="") as plik:
    # Tworze obiekt DictWriter, ktory zapisuje slowniki z kluczami nazwa i cena.
    writer = csv.DictWriter(plik, fieldnames=["nazwa", "cena"], delimiter=";")

    # Zapisuje pierwszy wiersz pliku jako naglowki kolumn.
    writer.writeheader()

    # Zapisuje wszystkie slowniki z listy jako kolejne wiersze pliku CSV.
    writer.writerows(produkty)

# Wyswietlam informacje, ze plik CSV zostal zapisany.
print(f"Zapisano produkty do pliku: {sciezka_pliku.name}")
