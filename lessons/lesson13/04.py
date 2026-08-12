import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "01" / "library.db"

with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT author, title, yearOfPublication FROM books WHERE author = ?",
        ("George Orwell",),
    )
    books = cursor.fetchall()
    for book in books:
        print(book)
