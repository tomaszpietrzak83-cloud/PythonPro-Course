import asyncio
from aiohttp import web
from lab_support import event, launch
from api_support import demo

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import SESSION, database, object_json, product_fields, positive_id

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

async def create_product(request):
    data = product_fields(await object_json(request))
    async with request.app[SESSION]() as session:
        async with session.begin():
            product = Product(name=data["name"], price=data["price"])
            session.add(product)
            await session.flush()
            result = product.to_dict()
        event("log", "transaction", "COMMIT: product saved")
    return web.json_response(result, status=201)

async def list_products(request):
    async with request.app[SESSION]() as session:
        statement = select(Product).order_by(Product.id)
        result = await session.execute(statement)
        products = result.scalars().all()
        return web.json_response([product.to_dict() for product in products])

async def get_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        product = await session.get(Product, product_id)
        if product is None:
            raise web.HTTPNotFound(text="Product not found")
        return web.json_response(product.to_dict())

async def delete_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        async with session.begin():
            product = await session.get(Product, product_id)
            if product is None:
                raise web.HTTPNotFound(text="Product not found")
            await session.delete(product)
    return web.Response(status=204)

async def main():
    async with database(Base) as factory:
        app = web.Application()
        app[SESSION] = factory
        app.router.add_post("/products", create_product)
        app.router.add_get("/products", list_products)
        app.router.add_get("/products/{id}", get_product)
        app.router.add_delete("/products/{id}", delete_product)
        await demo(app, [
            ('POST', '/products', {'name': 'Notebook', 'price': 1299}, 201),
            ('GET', '/products', None, 200),
            ('GET', '/products/1', None, 200),
            ('GET', '/products/999', None, 404),
            ('DELETE', '/products/1', None, 204),
            ('GET', '/products/1', None, 404),
        ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
