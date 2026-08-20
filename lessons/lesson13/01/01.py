import sqlite3
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from help_functions import sql_query_executioner

parentPath = Path(__file__).resolve().parent

filePath = parentPath / "library.db"

connection = sqlite3.connect(filePath)

cursor = connection.cursor()

query = """--sql
    CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    yearOfPublication INTEGER,
    UNIQUE(title, author, yearOfPublication)
)"""

sql_query_executioner(query, (), db_path=filePath)


connection.commit()
connection.close()
