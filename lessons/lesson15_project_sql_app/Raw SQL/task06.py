import sqlite3
from pathlib import Path

DATABASE_NAME = "todo_raw.db"

file_path = Path(__file__).parent.resolve()
database_path = file_path / DATABASE_NAME


def search_phrase(phrase):

    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM zadania WHERE opis LIKE ?", (f"%{phrase}%",))
        results = [row for row in cursor.fetchall()]
        return results
