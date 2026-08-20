import sqlite3
from pathlib import Path


def find_all_electronics_products():

    parentPath = Path(__file__).resolve().parent
    databasePath = parentPath / "shop.db"

    def findProductsByCategory(category_name):
        with sqlite3.connect(databasePath) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """--sql
                SELECT product_name, price
                FROM Products
                JOIN Categories ON Products.category_id = Categories.category_id
                WHERE Categories.category_name = ?
                """,
                (category_name,),
            )

            data = cursor.fetchall()

            result = []

            for row in data:
                result.append(f"Product: {row[0]}, Price: {row[1]}")
        return result

    return findProductsByCategory("Electronics")
