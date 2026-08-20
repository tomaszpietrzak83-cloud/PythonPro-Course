import sqlite3
from pathlib import Path


def display_customers_name_and_email():

    parentPath = Path(__file__).resolve().parent
    databasePath = parentPath / "shop.db"

    with sqlite3.connect(databasePath) as conn:
        cursor = conn.cursor()

        cursor.execute(""" --sql
            SELECT 
                name, email
            FROM Customers
            """)

        data = cursor.fetchall()

        result = []

        for row in data:
            result.append(f"Name: {row[0]}, Email: {row[1]}")

    return result
