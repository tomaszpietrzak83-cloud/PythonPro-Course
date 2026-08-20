import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "01" / "library.db"

# Fetch the book with the title "1984"
with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()

    cursor.execute(
        """--sql 
        SELECT * FROM books WHERE title = ?
        """,
        ("1984",),
    )

    book = cursor.fetchone()
    print(book)


# Change the year of publication to 1950
with sqlite3.connect(libraryPath) as connection:
    new_year_of_publication = 1950
    cursor = connection.cursor()

    cursor.execute(
        """--sql 
        UPDATE books SET yearOfPublication = ? WHERE title = ?
        """,
        (
            new_year_of_publication,
            "1984",
        ),
    )

    connection.commit()


# Check the changed book
with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()

    cursor.execute(
        """--sql 
        SELECT * FROM books WHERE title = ?
        """,
        ("1984",),
    )

    book = cursor.fetchone()
    print(book)


# Reset the year of publication to the original value
with sqlite3.connect(libraryPath) as connection:
    new_year_of_publication = 1949
    cursor = connection.cursor()

    # --sql
    cursor.execute(
        """--sql 
        UPDATE books SET yearOfPublication = ? WHERE title = ?
        """,
        (
            new_year_of_publication,
            "1984",
        ),
    )

    connection.commit()
