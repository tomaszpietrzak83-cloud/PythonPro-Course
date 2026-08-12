import sqlite3
from pathlib import Path

DATABASE_NAME = "todo_raw.db"

file_path = Path(__file__).parent.resolve()
database_path = file_path / DATABASE_NAME


def change_task_description(task_id, new_description):

    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        gr = """--sql
        UPDATE zadania SET opis = ? WHERE id = ?"""
        cursor.execute(gr, (new_description, task_id))
        print(f"Opis zadania {task_id} został zmieniony na: {new_description}")
