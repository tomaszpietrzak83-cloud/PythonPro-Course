import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT
        SUM(price) AS total_price
    FROM Products
    JOIN Categories ON Products.category_id = Categories.category_id
    WHERE Categories.category_name = 'Electronics'
    """)
    result = cursor.fetchone()
    print(f"Total price in Electronics: {result[0]}")
