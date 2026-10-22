import asyncio
from lab_support import launch, metric

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import database

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

async def main():
    async with database(Base) as factory:
        metric("Columns", str(list(Product.__table__.columns.keys())))
        metric("Price unit", "integer cents")

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
