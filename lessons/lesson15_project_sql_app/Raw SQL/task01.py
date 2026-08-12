import sqlite3
from pathlib import Path

DATABASE_NAME = "todo_raw.db"

file_path = Path(__file__).parent.resolve()
database_path = file_path / DATABASE_NAME


def delete_task(task_id):

    qr = """--sql DELETE FROM zadania WHERE id = ?"""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(qr, (task_id,))
        print(f"Zadanie o ID {task_id} zostało usunięte.")
