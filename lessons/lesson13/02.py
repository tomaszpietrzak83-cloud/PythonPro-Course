import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "01" / "library.db"


booksToAdd = [
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    ("To Kill a Mockingbird", "Harper Lee", 1960),
    ("1984", "George Orwell", 1949),
]
try:
    with sqlite3.connect(libraryPath) as connection:
        cursor = connection.cursor()
        cursor.executemany(
            """INSERT INTO books (title, author, yearOfPublication) VALUES (?, ?, ?)""",
            booksToAdd,
        )
        connection.commit()
except sqlite3.IntegrityError:
    print(f"Books already exists in the database: {booksToAdd}")
