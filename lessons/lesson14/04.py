import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT
        AVG(price) AS average_price
    FROM Products
    JOIN Categories ON Products.category_id = Categories.category_id
    WHERE Categories.category_name = 'Books'
    """)
    result = cursor.fetchone()
    print(f"Average price in Books: {result[0]}")
