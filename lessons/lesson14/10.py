import sqlite3
from pathlib import Path


class Product:
    def __init__(self, product_id, product_name, price):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price


def downloadProducts():
    with sqlite3.connect(databasePath) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """ --sql
            SELECT product_id, product_name, price
            FROM Products
            """,
        )
        result = cursor.fetchall()

        productsList = []
        for row in result:
            product = Product(row[0], row[1], row[2])
            productsList.append(product)

    return productsList


parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

products = downloadProducts()
for product in products:
    print(
        f"Product ID: {product.product_id}, Name: {product.product_name:25}, Price: {product.price:8.2f}"
    )
