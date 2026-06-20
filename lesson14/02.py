import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"

with sqlite3.connect(databasePath) as conn:
    cursor = conn.cursor()

    cursor.execute(""" --sql
    SELECT
        max(price) AS max_price
    FROM products
    """)
    result = cursor.fetchone()
    print(f"Max price: {result[0]}")
