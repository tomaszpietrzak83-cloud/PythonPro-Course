import sqlite3
from pathlib import Path

DATABASE_NAME = "todo_raw.db"


file_path = Path(__file__).parent.resolve()
database_path = file_path / DATABASE_NAME


def init_db():
    """Inicjalizuje bazę danych i tworzy tabelę, jeśli nie istnieje."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
    # Używamy IF NOT EXISTS, aby uniknąć błędu przy ponownym uruchomieniu
    cursor.execute("""--sql
    CREATE TABLE IF NOT EXISTS zadania (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opis TEXT NOT NULL,
    zrobione BOOLEAN NOT NULL CHECK (zrobione IN (0, 1)),
    _priority INTEGER DEFAULT 1)
    """)
    conn.commit()


def dodaj_zadanie(opis: str):
    """Dodaje nowe zadanie do bazy danych."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        # Używamy placeholderów (?), aby zapobiec SQL Injection
        cursor.execute(
            "INSERT INTO zadania (opis, zrobione) VALUES (?, ?)", (opis, False)
        )
    conn.commit()


def pobierz_zadania():
    """Pobiera wszystkie zadania z bazy danych."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, opis, zrobione FROM zadania")
    return cursor.fetchall()


def oznacz_jako_zrobione(id_zadania: int):
    """Oznacza zadanie o podanym ID jako zrobione."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE zadania SET zrobione = ? WHERE id = ?", (True, id_zadania)
        )
    conn.commit()
