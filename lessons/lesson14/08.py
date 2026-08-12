import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT
        Categories.category_name,
        COUNT(Products.product_id) AS quantity
    FROM Categories
    JOIN Products ON Categories.category_id = Products.category_id
    GROUP BY Categories.category_name
    ORDER BY quantity DESC
    """)

    result = cursor.fetchall()
    for row in result:
        print(f"Category: {row[0]}, Quantity: {row[1]}")
