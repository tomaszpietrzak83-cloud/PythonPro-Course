import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT product_name 
    FROM Products
    JOIN Orders_products ON Products.product_id = Orders_products.product_id
    JOIN Orders ON Orders_products.order_id = Orders.order_id
    JOIN Customers ON Orders.customer_id = Customers.customer_id
    WHERE Customers.name = 'Anna Nowak'
    """)
    result = cursor.fetchall()
    for row in result:
        print(f"Product: {row[0]}")
