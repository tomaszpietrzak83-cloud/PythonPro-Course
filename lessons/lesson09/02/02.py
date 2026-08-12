# Importuje klase Path z modulu pathlib, aby wygodnie pracowac ze sciezkami do plikow.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

try:
    # Pobieram od uzytkownika nazwe pliku, ktorego slowa maja zostac policzone.
    nazwa_pliku = input("Podaj nazwe pliku do odczytu: ")

    # Tworze obiekt Path z wpisanej przez uzytkownika nazwy pliku.
    sciezka_pliku = Path(nazwa_pliku)

    # Jesli uzytkownik podal tylko nazwe pliku, to szukam go w folderze tego skryptu.
    if not sciezka_pliku.is_absolute():
        # Lacze folder skryptu z nazwa pliku, aby uzyskac pelna sciezke lokalna.
        sciezka_pliku = folder_skryptu / sciezka_pliku

    # Otwieram wskazany plik w trybie odczytu z kodowaniem UTF-8.
    with sciezka_pliku.open("r", encoding="utf-8") as plik:
        # Wczytuje cala zawartosc pliku do jednego napisu.
        tekst = plik.read()

    # Dziele tekst na slowa i obliczam, ile slow znajduje sie w pliku.
    liczba_slow = len(tekst.split())

except FileNotFoundError:
    # Wyswietlam komunikat bledu, jesli podany plik nie istnieje.
    print("Nie znaleziono podanego pliku.")
else:
    # Wyswietlam obliczona liczbe slow, jesli odczyt pliku sie udal.
    print(f"Liczba slow w pliku: {liczba_slow}")

