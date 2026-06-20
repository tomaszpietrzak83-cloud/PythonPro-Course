import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "01" / "library.db"

# Fetch the book with the title "1984"
with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE title = ?", ("1984",))
    book = cursor.fetchone()
    print(book)

with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE books SET yearOfPublication = 1950 WHERE title = ?", ("1984",)
    )
    connection.commit()

with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE title = ?", ("1984",))
    book = cursor.fetchone()
    print(book)
# Reset the year of publication to the original value, for future runs of this code snippet
with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE books SET yearOfPublication = 1949 WHERE title = ?", ("1984",)
    )
    connection.commit()
