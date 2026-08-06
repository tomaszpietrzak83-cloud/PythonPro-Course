# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku dziennik.txt w tym samym folderze co skrypt.
sciezka_dziennika = folder_skryptu / "dziennik.txt"

# Uruchamiam petle nieskonczona, aby wielokrotnie pobierac kolejne linie od uzytkownika.
while True:
    # Pobieram jedna linie tekstu wpisana przez uzytkownika.
    linia = input('Wpisz jedna linie tekstu lub "koniec", aby zakonczyc program: ')

    # Sprawdzam, czy uzytkownik wpisal slowo konczace dzialanie programu.
    if linia.lower() == "koniec":
        # Przerywam petle, czyli koncze dzialanie programu.
        break

    # Otwieram plik w trybie dopisywania, aby nie usuwac wczesniejszych wpisow.
    with sciezka_dziennika.open("a", encoding="utf-8") as plik:
        # Dopisuje wpisana linie oraz znak nowej linii na koncu.
        plik.write(linia + "\n")

# Wyswietlam komunikat informujacy uzytkownika, gdzie zapisano wpisy.
print(f'Wpisy zostaly zapisane w pliku: {sciezka_dziennika.name}')

