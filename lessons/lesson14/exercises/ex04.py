import sqlite3
from pathlib import Path


def average_price_in_books():

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
    return result[0]
