# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

try:
    # Probuje zaimportowac klase Workbook z biblioteki openpyxl.
    from openpyxl import Workbook
except ModuleNotFoundError:
    # Ustawiam zmienna Workbook na None, jesli biblioteka openpyxl nie jest zainstalowana.
    Workbook = None

# Sprawdzam, czy biblioteka openpyxl jest dostepna w aktualnym srodowisku.
if Workbook is None:
    # Wyswietlam informacje, jak doinstalowac brakujaca biblioteke.
    print(
        'Brakuje biblioteki "openpyxl". Zainstaluj ja poleceniem: pip install openpyxl'
    )
else:
    # Tworze nowy skoroszyt Excela.
    skoroszyt = Workbook()

    # Pobieram aktywny arkusz z nowo utworzonego skoroszytu.
    arkusz = skoroszyt.active

    # Zmieniam nazwe arkusza na bardziej opisowa.
    arkusz.title = "Finanse"

    # Wpisuje nazwe pierwszego wydatku do komorki A1.
    arkusz["A1"] = "Czynsz"

    # Wpisuje wartosc pierwszego wydatku do komorki B1.
    arkusz["B1"] = 1500

    # Wpisuje nazwe drugiego wydatku do komorki A2.
    arkusz["A2"] = "Jedzenie"

    # Wpisuje wartosc drugiego wydatku do komorki B2.
    arkusz["B2"] = 600

    # Wpisuje etykiete sumy do komorki A3, aby bylo wiadomo, czego dotyczy wynik.
    arkusz["A3"] = "Suma"

    # Wstawiam formule Excela do komorki B3, aby zsumowac wartosci z komorek B1 i B2.
    arkusz["B3"] = "=SUM(B1:B2)"

    # Ustalam folder, w ktorym znajduje sie ten skrypt.
    folder_skryptu = Path(__file__).resolve().parent

    # Tworze sciezke do pliku finanse.xlsx w tym samym folderze co skrypt.
    sciezka_pliku = folder_skryptu / "finanse.xlsx"

    # Zapisuje skoroszyt do pliku Excela.
    skoroszyt.save(sciezka_pliku)

    # Wyswietlam informacje, ze plik Excel zostal utworzony.
    print(f"Utworzono plik Excela: {sciezka_pliku.name}")
