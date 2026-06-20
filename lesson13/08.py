import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "06" / "university.db"


with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute(""" --sql
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        studentId INTEGER NOT NULL,
        courseId INTEGER NOT NULL,
        FOREIGN KEY(studentId) REFERENCES students(id),
        FOREIGN KEY(courseId) REFERENCES courses(id),
        UNIQUE(studentId, courseId)
        )""")
