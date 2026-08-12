import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT product_name, price
    FROM Products
    WHERE price > (SELECT AVG(price) FROM Products)
    """)
    result = cursor.fetchall()
    for row in result:
        print(f"Product: {row[0]}, Price: {row[1]}")
