# Importuje modul json, aby odczytac dane zapisane w formacie JSON.
import json

# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku config.json utworzonego wczesniej w zadaniu 03.
sciezka_pliku = folder_skryptu.parent / "03" / "config.json"

try:
    # Otwieram plik konfiguracyjny w trybie odczytu.
    with sciezka_pliku.open("r", encoding="utf-8") as plik:
        # Wczytuje zawartosc pliku JSON i zamieniam ja na slownik Pythona.
        konfiguracja = json.load(plik)

except FileNotFoundError:
    # Informuje uzytkownika, ze najpierw trzeba uruchomic zadanie 03.
    print('Nie znaleziono pliku config.json. Najpierw uruchom skrypt z folderu "03".')
else:
    # Pobieram nazwe uzytkownika ze slownika konfiguracji.
    uzytkownik = konfiguracja["uzytkownik"]

    # Pobieram nazwe motywu ze slownika konfiguracji.
    motyw = konfiguracja["motyw"]

    # Wyswietlam komunikat z danymi odczytanymi z pliku JSON.
    print(f"Witaj, {uzytkownik}! Twoj motyw to {motyw}.")

