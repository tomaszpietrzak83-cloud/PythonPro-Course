import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT 
        name, email
    FROM Customers
    """)

    result = cursor.fetchall()
    for row in result:
        print(f"Name: {row[0]}, Email: {row[1]}")
