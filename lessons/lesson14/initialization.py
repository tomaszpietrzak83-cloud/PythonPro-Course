import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
databasePath = parentPath / "shop.db"


def prepare_database():
    """Creates and fills the database for exercises."""
    conn = sqlite3.connect(databasePath)  # Creates shop.db file
    cursor = conn.cursor()

    # Remove tables if they already exist for a clean start
    cursor.execute("DROP TABLE IF EXISTS Orders_Products")
    cursor.execute("DROP TABLE IF EXISTS Orders")
    cursor.execute("DROP TABLE IF EXISTS Products")
    cursor.execute("DROP TABLE IF EXISTS Categories")
    cursor.execute("DROP TABLE IF EXISTS Customers")

    # Creating tables
    cursor.execute("""
    CREATE TABLE Categories (
        category_id INTEGER PRIMARY KEY,
        category_name TEXT UNIQUE NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )""")

    cursor.execute("""
    CREATE TABLE Customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE Orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    )""")

    cursor.execute("""
    CREATE TABLE Orders_Products (
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )""")

    # Inserting data
    categories = [("Electronics",), ("Books",), ("Home and Garden",)]

    customers = [
        ("Anna Nowak", "anna.n@example.com"),
        ("Jan Kowalski", "jan.k@example.com"),
        ("Zofia Wiśniewska", "zofia.w@example.com"),
    ]

    products = [
        ("Laptop Pro", 5200.00, 1),
        ("Smartphone X", 2500.00, 1),
        ("Python for Everyone", 89.99, 2),
        ("Design Patterns", 120.50, 2),
        ("Electric Lawn Mower", 750.00, 3),
        ("Tool Set", 300.00, 3),
        ("Wireless Headphones", 450.00, 1),
    ]

    orders = [(1, "2023-10-01"), (2, "2023-10-02"), (1, "2023-10-05")]

    orders_products = [(1, 1, 1), (1, 7, 1), (2, 3, 2), (3, 5, 1)]

    cursor.executemany("INSERT INTO Categories (category_name) VALUES (?)", categories)

    cursor.executemany("INSERT INTO Customers (name, email) VALUES (?, ?)", customers)

    cursor.executemany(
        "INSERT INTO Products (product_name, price, category_id) VALUES (?, ?, ?)",
        products,
    )

    cursor.executemany(
        "INSERT INTO Orders (customer_id, order_date) VALUES (?, ?)", orders
    )

    cursor.executemany(
        "INSERT INTO Orders_Products (order_id, product_id, quantity) VALUES (?, ?, ?)",
        orders_products,
    )

    conn.commit()
    conn.close()

    print("Database 'shop.db' has been prepared.")


# Call the function to create the database before starting work
prepare_database()
