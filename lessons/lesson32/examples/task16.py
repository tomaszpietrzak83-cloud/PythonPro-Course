import asyncio
from aiohttp import web
from lab_support import launch
from api_support import demo

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from api_support import SESSION, database, object_json

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[int] = mapped_column(Integer)

class Transfer(Base):
    __tablename__ = "transfers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

async def transfer(request):
    data = await object_json(request)
    if set(data) != {"from_id", "to_id", "amount"}:
        raise web.HTTPBadRequest(text="from_id, to_id and amount required")
    if any(type(data[key]) is not int or not 1 <= data[key] <= 2147483647 for key in data):
        raise web.HTTPBadRequest(text="Use positive integers")
    if data["from_id"] == data["to_id"]:
        raise web.HTTPBadRequest(text="Accounts must differ")
    async with request.app[SESSION]() as session:
        async with session.begin():
            statement = select(Account).where(Account.id.in_([data["from_id"], data["to_id"]])).order_by(Account.id).with_for_update()
            accounts = (await session.execute(statement)).scalars().all()
            by_id = {account.id: account for account in accounts}
            if len(by_id) != 2:
                raise web.HTTPNotFound(text="Account not found")
            source = by_id[data["from_id"]]
            target = by_id[data["to_id"]]
            if source.balance < data["amount"]:
                raise web.HTTPConflict(text="Insufficient balance; transaction rolled back")
            source.balance -= data["amount"]
            await session.flush()
            if data["amount"] == 13:
                raise web.HTTPConflict(text="Demo failure after debit; transaction rolled back")
            target.balance += data["amount"]
            session.add(Transfer(description=f"Transfer {data['amount']} cents"))
    return web.json_response({"transferred": data["amount"]})

async def balances(request):
    async with request.app[SESSION]() as session:
        accounts = (await session.execute(select(Account).order_by(Account.id))).scalars().all()
        return web.json_response({str(account.id): account.balance for account in accounts})

async def main():
    async with database(Base) as factory:
        async with factory.begin() as session:
            session.add_all([Account(id=1, balance=1000), Account(id=2, balance=500)])
        app = web.Application()
        app[SESSION] = factory
        app.router.add_post("/transfer", transfer)
        app.router.add_get("/balances", balances)
        await demo(app, [
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 100}, 200),
            ("GET", "/balances", None, 200),
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 13}, 409),
            ("GET", "/balances", None, 200),
            ("POST", "/transfer", {"from_id": 1, "to_id": 2, "amount": 9999}, 409),
        ])

if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
