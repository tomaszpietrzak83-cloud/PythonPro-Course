import sqlite3
from pathlib import Path


def find_max_price():

    parentPath = Path(__file__).resolve().parent
    databasePath = parentPath / "shop.db"

    with sqlite3.connect(databasePath) as conn:
        cursor = conn.cursor()

        cursor.execute(""" --sql
                    
            SELECT
                product_name, MAX(price) AS max_price
            FROM products                   
                    
            -- SELECT product_name, price
            -- FROM products
            -- WHERE price = (SELECT MAX(price) FROM products)
                        
            """)
        result = cursor.fetchone()

    return (result[0], result[1])
