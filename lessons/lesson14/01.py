import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT
        COUNT(product_id) AS total_products
    FROM products
    """)
    result = cursor.fetchone()
    print(f"Total products: {result[0]}")
