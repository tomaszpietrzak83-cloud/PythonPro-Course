# Importujemy klase Session do typowania parametrow funkcji.
from sqlalchemy.orm import Session, selectinload
# Importujemy fabryke sesji bazy danych i walidacje schematu.
from sqlalchemy_app.database import SessionLocal, ensure_database_ready
# Importujemy modele ORM.
from sqlalchemy_app.models import Tag, Zadanie


# Funkcja wyswietla zadania razem z przypisanymi tagami.
def show_tasks(db: Session, tasks: list[Zadanie]) -> None:
    # Sprawdzamy, czy lista zadan nie jest pusta.
    if not tasks:
        # Informujemy uzytkownika, ze baza nie ma jeszcze rekordow.
        print("Brak zadan na liscie.")
        # Konczymy funkcje.
        return
    # Wypisujemy naglowek sekcji.
    print("\n--- Twoja lista zadan ---")
    # Iterujemy po zadaniach pobranych z bazy.
    for task in tasks:
        # Tworzymy prosty znacznik statusu zadania.
        status = "X" if task.zrobione else " "
        # Laczymy nazwy tagow jednym przecinkiem.
        tag_names = ", ".join(tag.nazwa for tag in task.tagi) or "brak tagow"
        # Wyswietlamy wszystkie najwazniejsze informacje o rekordzie.
        print(
            f"[{status}] ID: {task.id}, Opis: {task.opis}, "
            f"Tagi: {tag_names}, Utworzono: {task.creation_time}"
        )
    # Zamykamy sekcje wyswietlania.
    print("-------------------------\n")


# Funkcja dodaje nowe zadanie do bazy.
def add_task(db: Session, description: str) -> Zadanie:
    # Tworzymy nowy obiekt modelu ORM.
    new_task = Zadanie(opis=description)
    # Dodajemy obiekt do sesji.
    db.add(new_task)
    # Zatwierdzamy transakcje.
    db.commit()
    # Odswiezamy obiekt, aby mial np. wygenerowane ID.
    db.refresh(new_task)
    # Zwracamy gotowy obiekt.
    return new_task


# Funkcja usuwa zadanie po ID.
def delete_task(db: Session, task_id: int) -> bool:
    # Pobieramy pierwsze pasujace zadanie.
    task = db.query(Zadanie).filter(Zadanie.id == task_id).first()
    # Jesli nic nie znalezlismy, zwracamy False.
    if task is None:
        return False
    # Usuwamy obiekt z sesji.
    db.delete(task)
    # Zatwierdzamy usuniecie.
    db.commit()
    # Informujemy wywolujacego o sukcesie.
    return True


# Funkcja oznacza zadanie jako wykonane.
def mark_task_as_done(db: Session, task_id: int) -> bool:
    # Szukamy zadania po kluczu glownym.
    task = db.query(Zadanie).filter(Zadanie.id == task_id).first()
    # Jesli nie znalezlismy zadania, zwracamy False.
    if task is None:
        return False
    # Zmieniamy pole obiektu, a SQLAlchemy wygeneruje UPDATE.
    task.zrobione = True
    # Zatwierdzamy zmiane.
    db.commit()
    # Zwracamy sukces.
    return True


# Funkcja wyszukuje zadania po fragmencie opisu.
def search_tasks(db: Session, phrase: str) -> list[Zadanie]:
    # Budujemy zapytanie ORM z filtrem LIKE.
    tasks = (
        db.query(Zadanie)
        .options(selectinload(Zadanie.tagi))
        .filter(Zadanie.opis.like(f"%{phrase}%"))
        .order_by(Zadanie.id)
        .all()
    )
    # Zwracamy wszystkie dopasowania.
    return tasks


# Funkcja pobiera tag po nazwie lub tworzy go, jesli jeszcze nie istnieje.
def get_or_create_tag(db: Session, tag_name: str) -> Tag:
    # Usuwamy biale znaki z poczatku i konca nazwy.
    clean_name = tag_name.strip()
    # Szukamy istniejacego taga o tej nazwie.
    tag = db.query(Tag).filter(Tag.nazwa == clean_name).first()
    # Jesli tag juz istnieje, po prostu go zwracamy.
    if tag is not None:
        return tag
    # Tworzymy nowy obiekt modelu Tag.
    tag = Tag(nazwa=clean_name)
    # Dodajemy go do sesji.
    db.add(tag)
    # Zatwierdzamy, aby tag dostal ID.
    db.commit()
    # Odswiezamy obiekt po commicie.
    db.refresh(tag)
    # Zwracamy nowo utworzony tag.
    return tag


# Funkcja przypisuje tag do zadania.
def add_tag_to_task(db: Session, task_id: int, tag_name: str) -> bool:
    # Pobieramy zadanie razem z kolekcja tagow.
    task = (
        db.query(Zadanie)
        .options(selectinload(Zadanie.tagi))
        .filter(Zadanie.id == task_id)
        .first()
    )
    # Jesli zadanie nie istnieje, zwracamy False.
    if task is None:
        return False
    # Pobieramy istniejacy tag albo tworzymy nowy.
    tag = get_or_create_tag(db, tag_name)
    # Sprawdzamy, czy tag nie jest juz przypiety do zadania.
    if tag not in task.tagi:
        # Dodajemy obiekt Tag do relacji wiele-do-wielu.
        task.tagi.append(tag)
        # Zatwierdzamy nowe powiazanie w tabeli posredniej.
        db.commit()
    # Zwracamy sukces, bo zadanie istnialo i ma juz ten tag.
    return True


# Funkcja pobiera wszystkie zadania z tagami.
def get_all_tasks(db: Session) -> list[Zadanie]:
    # Budujemy zapytanie z dociaganiem relacji tagow.
    tasks = db.query(Zadanie).options(selectinload(Zadanie.tagi)).order_by(Zadanie.id).all()
    # Zwracamy gotowa liste obiektow.
    return tasks


# Funkcja pomocnicza pilnuje poprawnego odczytu liczby od uzytkownika.
def ask_for_task_id(message: str) -> int | None:
    # Probujemy sparsowac liczbe calkowita z inputu.
    try:
        # Zwracamy poprawne ID.
        return int(input(message))
    # Jesli input nie byl liczba, lapmy ValueError.
    except ValueError:
        # Informujemy uzytkownika o bledzie.
        print("Bledne ID. Podaj liczbe.")
        # Zwracamy None jako sygnal bledu.
        return None


# Funkcja main steruje cala aplikacja.
def main() -> None:
    # Sprawdzamy, czy baza i migracje sa gotowe przed otwarciem sesji.
    try:
        # Jesli schemat nie istnieje, dostaniemy czytelny komunikat.
        ensure_database_ready()
    # Lapiemy blad, aby pokazac go uzytkownikowi zamiast stack trace.
    except RuntimeError as error:
        # Wypisujemy instrukcje naprawy.
        print(error)
        # Konczymy program bez dalszej pracy.
        return

    # Tworzymy sesje bazy danych.
    db = SessionLocal()
    # Wchodzimy do bloku try, aby miec pewnosc zamkniecia sesji.
    try:
        # Startujemy glowna petle menu.
        while True:
            # Pokazujemy wszystkie opcje.
            print("Menu (SQLAlchemy + tagi):")
            print("1. Pokaz zadania")
            print("2. Dodaj zadanie")
            print("3. Usun zadanie")
            print("4. Oznacz zadanie jako zrobione")
            print("5. Wyszukaj zadanie")
            print("6. Dodaj tag do zadania")
            print("7. Wyjdz")
            # Pobieramy wybor uzytkownika.
            choice = input("Wybierz opcje: ").strip()

            # Opcja 1 pokazuje cala liste zadan.
            if choice == "1":
                # Pobieramy rekordy z bazy.
                tasks = get_all_tasks(db)
                # Wyswietlamy je w czytelnej formie.
                show_tasks(db, tasks)

            # Opcja 2 dodaje nowe zadanie.
            elif choice == "2":
                # Pobieramy opis od uzytkownika.
                description = input("Podaj opis zadania: ").strip()
                # Walidujemy pusty opis.
                if not description:
                    # Informujemy o problemie.
                    print("Opis zadania nie moze byc pusty.")
                    # Wracamy do menu.
                    continue
                # Dodajemy zadanie do bazy.
                task = add_task(db, description)
                # Potwierdzamy sukces.
                print(f"Zadanie dodane! Nowe ID: {task.id}")

            # Opcja 3 usuwa zadanie.
            elif choice == "3":
                # Pobieramy ID od uzytkownika.
                task_id = ask_for_task_id("Podaj ID zadania do usuniecia: ")
                # Wracamy do menu po blednym odczycie.
                if task_id is None:
                    continue
                # Usuwamy zadanie i sprawdzamy wynik.
                if delete_task(db, task_id):
                    # Potwierdzamy usuniecie.
                    print(f"Zadanie o ID {task_id} zostalo usuniete.")
                else:
                    # Informujemy, ze nie ma takiego zadania.
                    print("Zadanie o podanym ID nie istnieje.")

            # Opcja 4 oznacza zadanie jako wykonane.
            elif choice == "4":
                # Pobieramy ID zadania.
                task_id = ask_for_task_id("Podaj ID zadania do oznaczenia: ")
                # Wracamy do menu po bledzie.
                if task_id is None:
                    continue
                # Aktualizujemy rekord.
                if mark_task_as_done(db, task_id):
                    # Informujemy o sukcesie.
                    print("Zadanie zaktualizowane!")
                else:
                    # Informujemy o braku rekordu.
                    print("Nie znaleziono zadania o podanym ID.")

            # Opcja 5 wyszukuje zadania po frazie.
            elif choice == "5":
                # Pobieramy fraze od uzytkownika.
                phrase = input("Podaj fraze do wyszukania: ").strip()
                # Pobieramy wyniki z bazy.
                tasks = search_tasks(db, phrase)
                # Wyswietlamy dopasowania.
                show_tasks(db, tasks)

            # Opcja 6 dopina tag do wybranego zadania.
            elif choice == "6":
                # Pobieramy ID zadania.
                task_id = ask_for_task_id("Podaj ID zadania, do ktorego dodac tag: ")
                # Wracamy do menu po bledzie.
                if task_id is None:
                    continue
                # Pobieramy nazwe taga.
                tag_name = input("Podaj nazwe taga: ").strip()
                # Sprawdzamy, czy nazwa nie jest pusta.
                if not tag_name:
                    # Informujemy o problemie.
                    print("Nazwa taga nie moze byc pusta.")
                    # Wracamy do menu.
                    continue
                # Dodajemy tag do zadania.
                if add_tag_to_task(db, task_id, tag_name):
                    # Informujemy o sukcesie.
                    print("Tag zostal przypisany do zadania.")
                else:
                    # Informujemy, ze zadanie nie istnieje.
                    print("Nie znaleziono zadania o podanym ID.")

            # Opcja 7 konczy program.
            elif choice == "7":
                # Wyswietlamy krotkie pozegnanie.
                print("Do zobaczenia!")
                # Przerywamy petle.
                break

            # Obslugujemy wszystkie nieznane wartosci.
            else:
                # Informujemy o nieprawidlowej opcji.
                print("Nieznana opcja, sprobuj ponownie.")
    # Blok finally wykona sie zawsze, nawet po wyjatku.
    finally:
        # Zamykamy sesje bazy danych.
        db.close()


# Uruchamiamy main tylko przy bezposrednim odpaleniu pliku.
if __name__ == "__main__":
    # Startujemy aplikacje konsolowa.
    main()
