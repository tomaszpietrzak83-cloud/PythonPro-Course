# Importujemy modul sqlite3, bo pracujemy na bazie SQLite przez raw SQL.
import sqlite3

# Importujemy Path, aby wygodnie zbudowac sciezke do pliku bazy danych.
from pathlib import Path


# Definiujemy klase, ktora przejmie odpowiedzialnosc za cala obsluge bazy.
class TaskManagerRaw:
    # Konstruktor uruchamia sie przy tworzeniu obiektu klasy.
    def __init__(self, database_name: str = "todo_raw_class.db") -> None:
        # Zapamietujemy katalog, w ktorym lezy ten plik.
        self.base_dir = Path(__file__).resolve().parent
        # Budujemy pelna sciezke do pliku bazy danych.
        self.database_path = self.base_dir / database_name
        # Od razu tworzymy tabele, jesli jeszcze nie istnieja.
        self._initialize_database()

    # Prywatna metoda otwiera nowe polaczenie z baza.
    def _connect(self) -> sqlite3.Connection:
        # Tworzymy polaczenie z plikiem bazy danych.
        connection = sqlite3.connect(self.database_path)
        # Ustawiamy row_factory, aby odczytywac rekordy po nazwach kolumn.
        connection.row_factory = sqlite3.Row
        # Zwracamy gotowe polaczenie.
        return connection

    # Prywatna metoda przygotowuje strukture tabeli.
    def _initialize_database(self) -> None:
        # Otwieramy polaczenie w kontekscie, aby zamknelo sie automatycznie.
        with self._connect() as connection:
            # Wykonujemy SQL tworzacy tabele, jesli jej jeszcze nie ma.
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS zadania (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opis TEXT NOT NULL,
                    zrobione BOOLEAN NOT NULL DEFAULT 0 CHECK (zrobione IN (0, 1)),
                    priorytet INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            # Zatwierdzamy zmiany w bazie.
            connection.commit()

    # Ta metoda dodaje nowe zadanie i zwraca ID utworzonego rekordu.
    def add_task(self, description: str, priority: int = 1) -> int:
        # Otwieramy nowe polaczenie.
        with self._connect() as connection:
            # Tworzymy kursor do wykonywania zapytan.
            cursor = connection.cursor()
            # Dodajemy rekord, przekazujac wartosci przez placeholdery.
            cursor.execute(
                "INSERT INTO zadania (opis, zrobione, priorytet) VALUES (?, ?, ?)",
                (description, False, priority),
            )
            # Zapisujemy zmiany w bazie.
            connection.commit()
            # Zwracamy ID ostatnio dodanego rekordu.
            return int(cursor.lastrowid)

    # Ta metoda pobiera wszystkie zadania z bazy.
    def get_tasks(self) -> list[sqlite3.Row]:
        # Otwieramy polaczenie z baza.
        with self._connect() as connection:
            # Wykonujemy zapytanie i od razu pobieramy wszystkie rekordy.
            rows = connection.execute(
                "SELECT id, opis, zrobione, priorytet FROM zadania ORDER BY id"
            ).fetchall()
        # Zwracamy liste rekordow.
        return rows

    # Ta metoda usuwa zadanie o podanym ID.
    def delete_task(self, task_id: int) -> bool:
        # Otwieramy polaczenie z baza.
        with self._connect() as connection:
            # Tworzymy kursor.
            cursor = connection.cursor()
            # Usuwamy rekord o wskazanym ID.
            cursor.execute("DELETE FROM zadania WHERE id = ?", (task_id,))
            # Zatwierdzamy zmiany.
            connection.commit()
            # Zwracamy True tylko wtedy, gdy usunieto jakis rekord.
            return cursor.rowcount > 0

    # Ta metoda oznacza zadanie jako wykonane.
    def mark_task_as_done(self, task_id: int) -> bool:
        # Otwieramy polaczenie z baza.
        with self._connect() as connection:
            # Tworzymy kursor.
            cursor = connection.cursor()
            # Aktualizujemy pole `zrobione` dla podanego zadania.
            cursor.execute(
                "UPDATE zadania SET zrobione = ? WHERE id = ?",
                (True, task_id),
            )
            # Zatwierdzamy zmiany.
            connection.commit()
            # Zwracamy informacje, czy cos zostalo zaktualizowane.
            return cursor.rowcount > 0

    # Ta metoda wyszukuje zadania po fragmencie opisu.
    def search_tasks(self, phrase: str) -> list[sqlite3.Row]:
        # Otwieramy polaczenie z baza.
        with self._connect() as connection:
            # Wykonujemy zapytanie z operatorem LIKE.
            rows = connection.execute(
                """
                SELECT id, opis, zrobione, priorytet
                FROM zadania
                WHERE opis LIKE ?
                ORDER BY id
                """,
                (f"%{phrase}%",),
            ).fetchall()
        # Zwracamy liste pasujacych rekordow.
        return rows

    # Ta metoda zmienia opis istniejacego zadania.
    def update_task_description(
        self, task_id: int, new_description: str
    ) -> bool:
        # Otwieramy polaczenie z baza.
        with self._connect() as connection:
            # Tworzymy kursor.
            cursor = connection.cursor()
            # Aktualizujemy opis rekordu o wskazanym ID.
            cursor.execute(
                "UPDATE zadania SET opis = ? WHERE id = ?",
                (new_description, task_id),
            )
            # Zatwierdzamy zmiany.
            connection.commit()
            # Zwracamy True, jesli rekord zostal zmodyfikowany.
            return cursor.rowcount > 0
