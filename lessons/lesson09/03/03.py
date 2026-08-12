# Importuje modul json, aby zapisac slownik Pythona do pliku JSON.
import json

# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

# Tworze slownik z przykladowa konfiguracja aplikacji.
konfiguracja = {
    # Zapisuje nazwe uzytkownika w polu uzytkownik.
    "uzytkownik": "admin",
    # Zapisuje wybrany motyw interfejsu.
    "motyw": "ciemny",
    # Zapisuje rozdzielczosc ekranu jako liste dwoch liczb.
    "rozdzielczosc": [1920, 1080],
}

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku config.json w tym samym folderze co skrypt.
sciezka_pliku = folder_skryptu / "config.json"

# Otwieram plik do zapisu, aby utworzyc lub nadpisac plik JSON.
with sciezka_pliku.open("w", encoding="utf-8") as plik:
    # Zapisuje slownik do pliku JSON z wcieciami i bez zamiany polskich znakow na kody Unicode.
    json.dump(konfiguracja, plik, ensure_ascii=False, indent=4)

# Wyswietlam informacje, ze plik konfiguracyjny zostal zapisany.
print(f'Zapisano konfiguracje do pliku: {sciezka_pliku.name}')

