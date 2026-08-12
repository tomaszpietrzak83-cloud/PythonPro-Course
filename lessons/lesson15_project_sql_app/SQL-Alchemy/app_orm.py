from sqlalchemy.orm import Session
from sqlalchemy_app.database import get_db
from sqlalchemy_app.models import Zadanie
from task02 import delete_task
from task07 import search_phraze


def pokaz_zadania(db: Session):
    """Wyświetla listę wszystkich zadań."""
    zadania = db.query(Zadanie).all()  # Zamiast SELECT * FROM ...
    if not zadania:
        print("Brak zadań na liście.")
        return
    print("\n--- Twoja lista zadań ---")
    for zadanie in zadania:
        status = "✓" if zadanie.zrobione else "✗"
        print(f"[{status}] ID: {zadanie.id}, Opis: {zadanie.opis}")
    print("------------------------\n")


def dodaj_zadanie(db: Session, opis: str):
    """Dodaje nowe zadanie do bazy."""
    nowe_zadanie = Zadanie(opis=opis)  # Tworzymy obiekt, a nie piszemy INSERT
    db.add(nowe_zadanie)
    db.commit()
    db.refresh(nowe_zadanie)  # Odśwież, aby pobrać ID


def oznacz_jako_zrobione(db: Session, id_zadania: int):
    """Oznacza zadanie jako zrobione."""
    zadanie = (
        db.query(Zadanie).filter(Zadanie.id == id_zadania).first()
    )  # Wyszukujemy obiekt
    if zadanie:
        zadanie.zrobione = True  # Po prostu zmieniamy atrybut!
        db.commit()
        print("Zadanie zaktualizowane!")
    else:
        print("Nie znaleziono zadania o podanym ID.")


def main():
    db_generator = get_db()
    db_session = next(db_generator)
    while True:
        print("Menu (SQLAlchemy):")
        print("1. Pokaż zadania")
        print("2. Dodaj zadanie")
        print("3. Usuń zadanie")
        print("4. Oznacz zadanie jako zrobione")
        print("5. Wyszukaj zadanie")
        print("6. Wyjdź")
        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            pokaz_zadania(db_session)

        elif wybor == "2":
            opis = input("Podaj opis zadania: ")
            dodaj_zadanie(db_session, opis)
            print("Zadanie dodane!")

        elif wybor == "3":
            try:
                id_zadania = int(input("Podaj ID zadania do usunięcia: "))
                delete_task(db_session, id_zadania)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")

        elif wybor == "4":
            try:
                id_zadania = int(input("Podaj ID zadania do oznaczenia: "))
                oznacz_jako_zrobione(db_session, id_zadania)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == "5":
            phrase = input("Podaj frazę do wyszukania: ")
            results = search_phraze(db_session, phrase)
            if results:
                print("\n--- Wyniki wyszukiwania ---")
                for zadanie in results:
                    status = "✓" if zadanie.zrobione else "✗"
                    print(f"[{status}] ID: {zadanie.id}, Opis: {zadanie.opis}")
                print("-------------------------\n")
            else:
                print("Brak zadań pasujących do podanej frazy.")

        elif wybor == "6":
            print("Do zobaczenia!")
            db_session.close()
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")


if __name__ == "__main__":
    main()
