from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, default=0.0, nullable=False)

    def add_product(self, db: Session, name: str, price: float):
        existing = (
            db
            .query(Product)
            .filter(Product.name == name, Product.price == price)
            .first()
        )

        if existing:
            return "Product already exists"

        self.name = name
        self.price = price

        db.add(self)
        db.commit()
        db.refresh(self)
        return self
