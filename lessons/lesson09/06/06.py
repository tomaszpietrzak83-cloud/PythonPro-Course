# Importuje modul csv, aby odczytac dane z pliku CSV.
import csv

# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku produkty.csv utworzonego wczesniej w zadaniu 05.
sciezka_pliku = folder_skryptu.parent / "05" / "produkty.csv"

try:
    # Otwieram plik CSV do odczytu.
    with sciezka_pliku.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as plik:
        # Tworze czytnik DictReader, ktory zwraca kazdy wiersz jako slownik.
        reader = csv.DictReader(plik, delimiter=";")

        # Tworze zmienna startowa, w ktorej bede gromadzic sume cen wszystkich produktow.
        suma_cen = 0

        # Przechodze po kazdym wierszu odczytanym z pliku CSV.
        for wiersz in reader:
            # Zamieniam tekst z kolumny cena na liczbe typu float i dodaje ja do sumy.
            suma_cen += float(wiersz["cena"])

except FileNotFoundError:
    # Informuje uzytkownika, ze najpierw trzeba uruchomic zadanie 05.
    print('Nie znaleziono pliku produkty.csv. Najpierw uruchom skrypt z folderu "05".')
else:
    # Wyswietlam sume cen wszystkich produktow z dokladnoscia do dwoch miejsc po przecinku.
    print(f"Suma cen wszystkich produktow: {suma_cen:.2f} zl")
