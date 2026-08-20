import sqlite3
from pathlib import Path


def show_all_products_above_average():

    parentPath = Path(__file__).resolve().parent
    databasePath = parentPath / "shop.db"

    with sqlite3.connect(databasePath) as conn:
        cursor = conn.cursor()

        cursor.execute(""" --sql
            SELECT product_name, price
            FROM Products
            WHERE price > (SELECT AVG(price) FROM Products)
            """)
        data = cursor.fetchall()

        result = []
        for row in data:
            result.append(f"Product: {row[0]}, Price: {row[1]}")

    return result
