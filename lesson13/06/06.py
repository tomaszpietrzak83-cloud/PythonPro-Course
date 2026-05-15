import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent

filePath = parentPath / "university.db"

with sqlite3.connect(filePath) as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        UNIQUE(name, surname)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buildingName TEXT NOT NULL,
        numberOfClassroom TEXT NOT NULL,
        UNIQUE(buildingName, numberOfClassroom)
    )""")
