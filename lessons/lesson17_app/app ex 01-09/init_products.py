from database import SessionLocal, engine
from models import Base, Product

SAMPLE_PRODUCTS = [
    ("Laptop", 999.99),
    ("Phone", 599.99),
    ("Headphones", 199.99),
    ("Smartwatch", 299.99),
    ("Tablet", 399.99),
    ("Camera", 499.99),
    ("Printer", 149.99),
    ("Monitor", 249.99),
    ("Keyboard", 89.99),
    ("Mouse", 49.99),
]


def seed_products():
    Base.metadata.create_all(bind=engine)

    added_count = 0
    skipped_count = 0

    with SessionLocal() as db:
        for name, price in SAMPLE_PRODUCTS:
            result = Product().add_product(db, name=name, price=price)
            if isinstance(result, str):
                skipped_count += 1
            else:
                added_count += 1

        total_count = db.query(Product).count()

    print(f"Added products: {added_count}")
    print(f"Skipped existing products: {skipped_count}")
    print(f"Total products in database: {total_count}")


if __name__ == "__main__":
    seed_products()
