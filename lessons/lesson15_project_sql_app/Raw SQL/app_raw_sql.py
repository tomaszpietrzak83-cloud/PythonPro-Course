import database_raw as db
from task01 import delete_task
from task06 import search_phrase
from task10 import change_task_description


def pokaz_zadania():
    """Wyświetla listę wszystkich zadań."""
    zadania = db.pobierz_zadania()
    if not zadania:
        print("Brak zadań na liście.")
        return
    print("\n--- Twoja lista zadań ---")
    for zadanie in zadania:
        status = "✓" if zadanie[2] else "✗"
        print(f"[{status}] ID: {zadanie[0]}, Opis: {zadanie[1]}")
    print("------------------------\n")


def main():
    db.init_db()  # Upewnij się, że baza i tabela istnieją
    while True:
        print("Menu:")
        print("1. Pokaż zadania")
        print("2. Dodaj zadanie")
        print("3. Usuń zadanie")
        print("4. Oznacz zadanie jako zrobione")
        print("5. Wyszukaj zadanie")
        print("6. Zmień opis zadania")
        print("7. Wyjdź")
        wybor = input("Wybierz opcję: ")
        if wybor == "1":
            pokaz_zadania()
        elif wybor == "2":
            opis = input("Podaj opis zadania: ")
            db.dodaj_zadanie(opis)
            print("Zadanie dodane!")
        elif wybor == "3":
            try:
                id_zadania = int(input("Podaj ID zadania do usunięcia: "))
                delete_task(id_zadania)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == "4":
            try:
                id_zadania = int(input("Podaj ID zadania do oznaczenia: "))
                db.oznacz_jako_zrobione(id_zadania)
                print("Zadanie zaktualizowane!")
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == "5":
            phrase = input("Podaj frazę do wyszukania: ")
            results = search_phrase(phrase)
            if results:
                print("\n--- Wyniki wyszukiwania ---")
                for zadanie in results:
                    status = "✓" if zadanie[2] else "✗"
                    print(f"[{status}] ID: {zadanie[0]}, Opis: {zadanie[1]}")
                print("-------------------------\n")
            else:
                print("Brak zadań pasujących do frazy.")

        elif wybor == "6":
            try:
                id_zadania = int(input("Podaj ID zadania do zmiany opisu: "))
                new_description = input("Podaj nowy opis zadania: ")
                change_task_description(id_zadania, new_description)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")

        elif wybor == "7":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")


if __name__ == "__main__":
    main()
