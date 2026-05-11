# Importuje modul json, aby zapisywac i odczytywac liste zadan z pliku.
import json

# Importuje klase Path z modulu pathlib, aby wygodnie zbudowac sciezke do pliku.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do pliku zadania.json w tym samym folderze co skrypt.
sciezka_pliku = folder_skryptu / "zadania.json"


# Definiuje funkcje, ktora wczytuje liste zadan z pliku JSON.
def wczytaj_zadania():
    # Sprawdzam, czy plik z zadaniami juz istnieje.
    if sciezka_pliku.exists():
        # Otwieram istniejacy plik do odczytu.
        with sciezka_pliku.open("r", encoding="utf-8") as plik:
            # Wczytuje dane JSON i zwracam je jako liste Pythona.
            return json.load(plik)

    # Zwracam pusta liste, jesli plik jeszcze nie istnieje.
    return []


# Definiuje funkcje, ktora zapisuje aktualna liste zadan do pliku JSON.
def zapisz_zadania(lista_zadan):
    # Otwieram plik do zapisu, aby utworzyc go lub nadpisac aktualna zawartosc.
    with sciezka_pliku.open("w", encoding="utf-8") as plik:
        # Zapisuje liste zadan w pliku JSON z wcieciami i polskimi znakami.
        json.dump(lista_zadan, plik, ensure_ascii=False, indent=4)


# Definiuje funkcje, ktora wyswietla wszystkie zapisane zadania.
def wyswietl_zadania(lista_zadan):
    # Sprawdzam, czy lista zadan jest pusta.
    if not lista_zadan:
        # Informuje uzytkownika, ze nie ma jeszcze zadnych zadan.
        print("Lista zadan jest pusta.")
        # Koncze dzialanie tej funkcji, bo nie ma czego wyswietlac dalej.
        return

    # Wyswietlam naglowek sekcji z zadaniami.
    print("\nTwoje zadania:")

    # Przechodze po liscie zadan razem z ich numerami rozpoczynajacymi sie od 1.
    for numer, zadanie in enumerate(lista_zadan, start=1):
        # Wyswietlam numer zadania i jego tresc.
        print(f"{numer}. {zadanie}")


# Wczytuje liste zadan z pliku przy starcie programu.
zadania = wczytaj_zadania()

# Uruchamiam petle nieskonczona, aby program dzialal do momentu wybrania opcji wyjscia.
while True:
    # Wyswietlam menu z dostepnymi opcjami programu.
    print("\n1. Dodaj zadanie")
    print("2. Wyswietl zadania")
    print("3. Zapisz zadania")
    print("4. Zakoncz program")

    # Pobieram od uzytkownika numer wybranej opcji.
    wybor = input("Wybierz opcje: ")

    # Sprawdzam, czy uzytkownik chce dodac nowe zadanie.
    if wybor == "1":
        # Pobieram tresc nowego zadania wpisana przez uzytkownika.
        nowe_zadanie = input("Podaj tresc nowego zadania: ")

        # Dodaje nowe zadanie na koniec listy zadan.
        zadania.append(nowe_zadanie)

        # Informuje uzytkownika, ze zadanie zostalo dodane.
        print("Dodano nowe zadanie.")

    # Sprawdzam, czy uzytkownik chce wyswietlic wszystkie zadania.
    elif wybor == "2":
        # Wywoluje funkcje wyswietlajaca aktualna liste zadan.
        wyswietl_zadania(zadania)

    # Sprawdzam, czy uzytkownik chce recznie zapisac zadania do pliku.
    elif wybor == "3":
        # Zapisuje aktualna liste zadan do pliku JSON.
        zapisz_zadania(zadania)

        # Informuje uzytkownika, ze zapis sie udal.
        print("Zadania zostaly zapisane.")

    # Sprawdzam, czy uzytkownik chce zakonczyc dzialanie programu.
    elif wybor == "4":
        # Zapisuje zadania przed zamknieciem programu.
        zapisz_zadania(zadania)

        # Informuje uzytkownika, ze zadania zostaly zapisane przy wyjsciu.
        print("Zadania zostaly zapisane. Program konczy dzialanie.")

        # Przerywam petle, aby zakonczyc program.
        break

    # Obsluguje sytuacje, gdy uzytkownik poda niepoprawny numer opcji.
    else:
        # Wyswietlam komunikat o blednym wyborze.
        print("Niepoprawna opcja. Sprobuj ponownie.")

