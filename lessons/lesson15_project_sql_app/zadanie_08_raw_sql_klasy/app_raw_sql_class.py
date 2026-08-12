# Importujemy klase, ktora obsluguje baze danych.
from task_manager_raw import TaskManagerRaw


# Funkcja wyswietla liste zadan w czytelnej formie.
def show_tasks(task_manager: TaskManagerRaw, tasks: list) -> None:
    # Sprawdzamy, czy lista jest pusta.
    if not tasks:
        # Informujemy uzytkownika, ze nic jeszcze nie ma w bazie.
        print("Brak zadan na liscie.")
        # Konczymy funkcje szybkim wyjsciem.
        return
    # Wypisujemy naglowek sekcji.
    print("\n--- Twoja lista zadan ---")
    # Przechodzimy po wszystkich rekordach.
    for task in tasks:
        # Zamieniamy wartosc bool na prosty znak statusu.
        status = "X" if task["zrobione"] else " "
        # Wyswietlamy najwazniejsze dane zadania.
        print(
            f"[{status}] ID: {task['id']}, Priorytet: {task['priorytet']}, "
            f"Opis: {task['opis']}"
        )
    # Zamykamy sekcje wyswietlania.
    print("-------------------------\n")


# Funkcja zbiera od uzytkownika ID i pilnuje poprawnej konwersji na int.
def ask_for_task_id(message: str) -> int | None:
    # Probujemy zamienic wpisany tekst na liczbe calkowita.
    try:
        # Zwracamy poprawnie sparsowane ID.
        return int(input(message))
    # Gdy uzytkownik wpisze cos, co nie jest liczba, lapiemy blad.
    except ValueError:
        # Informujemy o problemie.
        print("Bledne ID. Podaj liczbe.")
        # Zwracamy None, aby wywolujacy wiedzial, ze odczyt sie nie udal.
        return None


# Funkcja main steruje cala aplikacja konsolowa.
def main() -> None:
    # Tworzymy obiekt klasy, a konstruktor sam inicjalizuje baze.
    task_manager = TaskManagerRaw()
    # Uruchamiamy petle menu.
    while True:
        # Wyswietlamy dostepne opcje.
        print("Menu (Raw SQL + klasy):")
        print("1. Pokaz zadania")
        print("2. Dodaj zadanie")
        print("3. Usun zadanie")
        print("4. Oznacz zadanie jako zrobione")
        print("5. Wyszukaj zadanie")
        print("6. Zmien opis zadania")
        print("7. Wyjdz")
        # Pobieramy wybor uzytkownika.
        choice = input("Wybierz opcje: ").strip()

        # Opcja 1 pobiera i wyswietla wszystkie zadania.
        if choice == "1":
            # Wywolujemy metode klasy do pobrania wszystkich rekordow.
            tasks = task_manager.get_tasks()
            # Przekazujemy wynik do funkcji wyswietlajacej.
            show_tasks(task_manager, tasks)

        # Opcja 2 dodaje nowe zadanie.
        elif choice == "2":
            # Pobieramy opis od uzytkownika.
            description = input("Podaj opis zadania: ").strip()
            # Sprawdzamy, czy opis nie jest pusty.
            if not description:
                # Informujemy, ze pusty opis nie ma sensu.
                print("Opis zadania nie moze byc pusty.")
                # Przechodzimy do kolejnej iteracji petli.
                continue
            # Dodajemy zadanie i zapamietujemy ID nowego rekordu.
            task_id = task_manager.add_task(description)
            # Informujemy o sukcesie.
            print(f"Zadanie dodane! Nowe ID: {task_id}")

        # Opcja 3 usuwa zadanie.
        elif choice == "3":
            # Pobieramy ID zadania od uzytkownika.
            task_id = ask_for_task_id("Podaj ID zadania do usuniecia: ")
            # Jesli parsowanie sie nie udalo, wracamy do menu.
            if task_id is None:
                continue
            # Probujemy usunac zadanie i sprawdzamy wynik.
            if task_manager.delete_task(task_id):
                # Potwierdzamy usuniecie.
                print(f"Zadanie o ID {task_id} zostalo usuniete.")
            else:
                # Informujemy, ze nie znaleziono rekordu.
                print("Zadanie o podanym ID nie istnieje.")

        # Opcja 4 oznacza zadanie jako zrobione.
        elif choice == "4":
            # Pobieramy ID od uzytkownika.
            task_id = ask_for_task_id("Podaj ID zadania do oznaczenia: ")
            # Jesli nie udalo sie wczytac liczby, wracamy do menu.
            if task_id is None:
                continue
            # Wywolujemy metode aktualizujaca status zadania.
            if task_manager.mark_task_as_done(task_id):
                # Informujemy o sukcesie.
                print("Zadanie zaktualizowane!")
            else:
                # Informujemy o braku pasujacego rekordu.
                print("Nie znaleziono zadania o podanym ID.")

        # Opcja 5 wyszukuje zadania po fragmencie opisu.
        elif choice == "5":
            # Pobieramy fraze od uzytkownika.
            phrase = input("Podaj fraze do wyszukania: ").strip()
            # Wyszukujemy pasujace rekordy.
            results = task_manager.search_tasks(phrase)
            # Wyswietlamy wyniki przez te sama funkcje co zwykla liste.
            show_tasks(task_manager, results)

        # Opcja 6 zmienia opis wybranego zadania.
        elif choice == "6":
            # Pobieramy ID zadania.
            task_id = ask_for_task_id("Podaj ID zadania do zmiany opisu: ")
            # Wracamy do menu, jesli ID bylo bledne.
            if task_id is None:
                continue
            # Pobieramy nowy opis.
            new_description = input("Podaj nowy opis zadania: ").strip()
            # Pilnujemy, by nowy opis nie byl pusty.
            if not new_description:
                # Informujemy o problemie.
                print("Nowy opis nie moze byc pusty.")
                # Wracamy do petli menu.
                continue
            # Probujemy zmienic opis zadania.
            if task_manager.update_task_description(task_id, new_description):
                # Potwierdzamy zmiane.
                print("Opis zadania zostal zaktualizowany.")
            else:
                # Informujemy o braku rekordu.
                print("Nie znaleziono zadania o podanym ID.")

        # Opcja 7 konczy dzialanie programu.
        elif choice == "7":
            # Wyswietlamy pozegnanie.
            print("Do zobaczenia!")
            # Przerywamy petle while.
            break

        # Kazda inna wartosc jest niepoprawna.
        else:
            # Informujemy o blednym wyborze.
            print("Nieznana opcja, sprobuj ponownie.")


# Ten warunek uruchamia main tylko wtedy, gdy plik odpalasz bezposrednio.
if __name__ == "__main__":
    # Startujemy aplikacje.
    main()
