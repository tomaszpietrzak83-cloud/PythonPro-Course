from database import SessionLocal
from models import Product

db = SessionLocal()
try:
    Product().add_product(db, name="Laptop", price=999.99)
    Product().add_product(db, name="Phone", price=599.99)
    Product().add_product(db, name="Headphones", price=199.99)
    Product().add_product(db, name="Smartwatch", price=299.99)
    Product().add_product(db, name="Tablet", price=399.99)
    Product().add_product(db, name="Camera", price=499.99)
    Product().add_product(db, name="Printer", price=149.99)
    Product().add_product(db, name="Monitor", price=249.99)
    Product().add_product(db, name="Keyboard", price=89.99)
    Product().add_product(db, name="Mouse", price=49.99)
finally:
    db.close()
