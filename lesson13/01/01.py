import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent

filePath = parentPath / "library.db"

connection = sqlite3.connect(filePath)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    yearOfPublication INTEGER,
    UNIQUE(title, author, yearOfPublication)
)""")

connection.commit()
