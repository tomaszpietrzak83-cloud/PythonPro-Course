import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import SESSION, database, positive_id

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

async def get_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        statement = select(Product, User).join(User).where(Product.id == product_id)
        result = await session.execute(statement)
        row = result.one_or_none()
        if row is None:
            raise web.HTTPNotFound(text="Product not found")
        product, user = row
        return web.json_response({"id": product.id, "name": product.name, "price": product.price, "creator": user.username})

async def main():
    async with database(Base) as factory:
        async with factory.begin() as session:
            user = User(username="Anna")
            session.add(user)
            await session.flush()
            session.add(Product(name="Notebook", price=1299, user_id=user.id))
        app = web.Application()
        app[SESSION] = factory
        app.router.add_get("/products/{id}", get_product)
        await demo(app, [
            ('GET', '/products/1', None, 200),
            ('GET', '/products/99', None, 404),
        ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
