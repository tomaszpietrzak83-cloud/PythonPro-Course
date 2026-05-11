# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezki do plikow.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku log.txt, z ktorego bede czytac dane.
sciezka_logu = folder_skryptu / "log.txt"

# Tworze sciezke do pliku wynikowego, do ktorego zapisze znalezione linie.
sciezka_wynikow = folder_skryptu / "wyniki_wyszukiwania.txt"

# Pobieram od uzytkownika slowo, ktorego program ma szukac w pliku logow.
szukane_slowo = input("Podaj slowo do wyszukania w pliku log.txt: ")

try:
    # Otwieram plik log.txt do odczytu.
    with sciezka_logu.open("r", encoding="utf-8") as plik_logu:
        # Otwieram plik wynikowy do zapisu, aby zapisac do niego pasujace linie.
        with sciezka_wynikow.open("w", encoding="utf-8") as plik_wynikowy:
            # Tworze licznik znalezionych linii i ustawiam go na zero.
            liczba_znalezionych_linii = 0

            # Przechodze po kazdej linii odczytanej z pliku logow.
            for linia in plik_logu:
                # Sprawdzam, czy w aktualnej linii znajduje sie szukane slowo.
                if szukane_slowo in linia:
                    # Zapisuje pasujaca linie do pliku wynikowego.
                    plik_wynikowy.write(linia)

                    # Zwiekszam licznik znalezionych linii o jeden.
                    liczba_znalezionych_linii += 1

except FileNotFoundError:
    # Informuje uzytkownika, ze plik log.txt nie istnieje w folderze skryptu.
    print('Nie znaleziono pliku log.txt. Umiesc go w folderze "08" i uruchom program ponownie.')
else:
    # Wyswietlam informacje, ile linii zapisano do pliku wynikowego.
    print(f'Zapisano {liczba_znalezionych_linii} pasujacych linii do pliku: {sciezka_wynikow.name}')

