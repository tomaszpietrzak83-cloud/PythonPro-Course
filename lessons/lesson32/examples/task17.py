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
        page = positive_id(request.query.get("page", "1"))
        limit = positive_id(request.query.get("limit", "10"))
        if limit > 100:
            raise web.HTTPBadRequest(text="limit must not exceed 100")
        offset = (page - 1) * limit
        statement = select(Product).order_by(Product.id).offset(offset).limit(limit)
        result = await session.execute(statement)
        products = result.scalars().all()
        return web.json_response([product.to_dict() for product in products])

async def main():
    async with database(Base) as factory:
        app = web.Application()
        app[SESSION] = factory
        app.router.add_post("/products", create_product)
        app.router.add_get("/products", list_products)
        await demo(app, [
            ('POST', '/products', {'name': 'Notebook', 'price': 1299}, 201),
            ('GET', '/products', None, 200),
            ('POST', '/products', {'name': 'Pen', 'price': 250}, 201),
            ('GET', '/products?page=2&limit=1', None, 200),
            ('GET', '/products?page=0', None, 400),
        ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
