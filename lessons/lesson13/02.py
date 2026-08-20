import sqlite3
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from help_functions import sql_query_executioner

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "01" / "library.db"


booksToAdd = [
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    ("To Kill a Mockingbird", "Harper Lee", 1960),
    ("1984", "George Orwell", 1949),
]

query = """--sql
 INSERT INTO books (title, author, yearOfPublication) VALUES (?, ?, ?)
 """

try:
    sql_query_executioner(query, booksToAdd, db_path=libraryPath)
except sqlite3.IntegrityError:
    print(f"Books already exists in the database: {booksToAdd}")
