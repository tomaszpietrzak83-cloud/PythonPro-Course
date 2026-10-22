"""Explicit authoring script; generates independent, readable exercise files."""
import ast
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
HEADER = '''import asyncio
from aiohttp import web
from lab_support import event, launch, metric, span
from api_support import demo
'''
ENTRY = '''
if __name__ == "__main__":
    launch(lambda options: asyncio.run(main()))
'''
MODEL = '''
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
'''
CREATE = '''
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
'''
LIST = '''
async def list_products(request):
    async with request.app[SESSION]() as session:
        statement = select(Product).order_by(Product.id)
        result = await session.execute(statement)
        products = result.scalars().all()
        return web.json_response([product.to_dict() for product in products])
'''
GET = '''
async def get_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        product = await session.get(Product, product_id)
        if product is None:
            raise web.HTTPNotFound(text="Product not found")
        return web.json_response(product.to_dict())
'''


def save(number, code):
    code=dedent(code).strip() + '\n' + ENTRY
    tree=ast.parse(code)
    used={node.id for node in ast.walk(tree) if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load)}
    cleaned=[]
    imports={node.lineno:node for node in tree.body if isinstance(node,(ast.Import,ast.ImportFrom))}
    for index,line in enumerate(code.splitlines(),1):
        if index in imports:
            node=imports[index]
            node.names=[alias for alias in node.names if (alias.asname or alias.name.split('.')[0]) in used]
            if node.names:
                cleaned.append(ast.unparse(node))
        else:
            cleaned.append(line)
    code='\n'.join(cleaned)
    lines=[]
    for line in code.splitlines():
        stripped=line.strip()
        if stripped.startswith('await demo(app, [') and stripped.endswith('])'):
            cases=ast.literal_eval(ast.parse(stripped).body[0].value.value.args[1])
            indent=line[:len(line)-len(line.lstrip())]
            lines.append(indent+'await demo(app, [')
            lines.extend(indent+'    '+repr(case)+',' for case in cases)
            lines.append(indent+'])')
        else:
            lines.append(line)
    (ROOT / 'examples' / f'task{number:02}.py').write_text('\n'.join(lines)+'\n', encoding='utf-8')


def db_main(routes, cases):
    return '\nasync def main():\n    async with database(Base) as factory:\n        app = web.Application()\n        app[SESSION] = factory\n' + ''.join(f'        app.router.add_{method}("{path}", {handler})\n' for method,path,handler in routes) + f'        await demo(app, {cases!r})\n'


def main():
    save(1, HEADER + '''
async def operation(name, delay):
    with span(name, "Waiting for I/O"):
        await asyncio.sleep(delay)
        return delay

async def main():
    results = await asyncio.gather(operation("A", 1), operation("B", 4), operation("C", 2))
    metric("Delays in input order", str(results))
''')
    simple = {
        2: ('/', 'async def hello(request):\n    return web.Response(text="<h1>Welcome to my page!</h1>", content_type="text/html")', 'hello', [('GET','/',None,200)]),
        3: ('/witaj/{name}', 'async def hello(request):\n    name = request.match_info["name"]\n    return web.Response(text=f"Hello, {name}!")', 'hello', [('GET','/witaj/Anna',None,200)]),
        4: ('/api/status', 'from datetime import datetime\n\nasync def status(request):\n    now = datetime.now().isoformat()\n    return web.json_response({"status": "OK", "server_time": now})', 'status', [('GET','/api/status',None,200)]),
        5: ('/api/search', 'async def search(request):\n    query = request.query.get("q")\n    if query is None:\n        return web.json_response({"error": "Missing q parameter"}, status=400)\n    return web.json_response({"search_query": query})', 'search', [('GET','/api/search?q=python',None,200),('GET','/api/search',None,400)]),
        6: ('/api/echo', 'import json\n\nasync def echo(request):\n    try:\n        data = await request.json()\n    except (json.JSONDecodeError, UnicodeDecodeError):\n        raise web.HTTPBadRequest(text="Invalid JSON")\n    return web.json_response(data)', 'echo', [('POST','/api/echo',{'message':'Python'},200)]),
        8: ('/witaj/{name}', 'async def hello(request):\n    name = request.match_info["name"]\n    if name == "admin":\n        raise web.HTTPForbidden(text="Admin access forbidden")\n    return web.Response(text=f"Hello, {name}!")', 'hello', [('GET','/witaj/Anna',None,200),('GET','/witaj/admin',None,403)]),
    }
    for n,(path,handler,name,cases) in simple.items():
        method = 'post' if n == 6 else 'get'
        save(n, HEADER + '\n' + handler + f'\n\nasync def main():\n    app = web.Application()\n    app.router.add_{method}("{path}", {name})\n    await demo(app, {cases!r})\n')
    save(7, HEADER + MODEL + '''
async def main():
    async with database(Base) as factory:
        metric("Columns", str(list(Product.__table__.columns.keys())))
        metric("Price unit", "integer cents")
''')
    create_case = ('POST','/products',{'name':'Notebook','price':1299},201)
    base_routes = [('post','/products','create_product')]
    for n in (9,10,11,14,15,17,19):
        code = HEADER + MODEL + CREATE
        routes = base_routes.copy(); cases = [create_case]
        if n in (10,11,14,15,17,19):
            code += LIST; routes += [('get','/products','list_products')]
            cases += [('GET','/products',None,200)]
        if n in (11,14,15,19):
            code += GET; routes += [('get','/products/{id}','get_product')]
            cases += [('GET','/products/1',None,200),('GET','/products/999',None,404)]
        if n == 14:
            code += '''
async def update_product(request):
    product_id = positive_id(request.match_info["id"])
    data = product_fields(await object_json(request), partial=True)
    async with request.app[SESSION]() as session:
        async with session.begin():
            product = await session.get(Product, product_id)
            if product is None:
                raise web.HTTPNotFound(text="Product not found")
            if "name" in data:
                product.name = data["name"]
            if "price" in data:
                product.price = data["price"]
            await session.flush()
            result = product.to_dict()
    return web.json_response(result)
'''
            routes += [('patch','/products/{id}','update_product')]
            cases += [('PATCH','/products/1',{'price':999},200),('GET','/products/1',None,200)]
        if n == 15:
            code += '''
async def delete_product(request):
    product_id = positive_id(request.match_info["id"])
    async with request.app[SESSION]() as session:
        async with session.begin():
            product = await session.get(Product, product_id)
            if product is None:
                raise web.HTTPNotFound(text="Product not found")
            await session.delete(product)
    return web.Response(status=204)
'''
            routes += [('delete','/products/{id}','delete_product')]
            cases += [('DELETE','/products/1',None,204),('GET','/products/1',None,404)]
        if n == 17:
            start=code.index('        statement = select(Product)')
            end=code.index('        result =',start)
            code=code[:start]+'''        page = positive_id(request.query.get("page", "1"))
        limit = positive_id(request.query.get("limit", "10"))
        if limit > 100:
            raise web.HTTPBadRequest(text="limit must not exceed 100")
        offset = (page - 1) * limit
        statement = select(Product).order_by(Product.id).offset(offset).limit(limit)
'''+code[end:]
            cases += [('POST','/products',{'name':'Pen','price':250},201),('GET','/products?page=2&limit=1',None,200),('GET','/products?page=0',None,400)]
        if n == 19:
            (ROOT/'examples'/'routes.py').write_text('"""Routing for task19; handlers are supplied explicitly to avoid circular imports."""\n\ndef setup_routes(app, create_product, list_products, get_product):\n    app.router.add_post("/products", create_product)\n    app.router.add_get("/products", list_products)\n    app.router.add_get("/products/{id}", get_product)\n',encoding='utf-8')
            code += '''
from routes import setup_routes

def create_app(factory):
    app = web.Application()
    app[SESSION] = factory
    setup_routes(app, create_product, list_products, get_product)
    return app
'''
            tail='\nasync def main():\n    async with database(Base) as factory:\n        app = create_app(factory)\n' + f'        await demo(app, {cases!r})\n'
        else:
            tail=db_main(routes,cases)
        save(n,code+tail)
    save(12, HEADER + '''
from aiohttp import ClientSession, ClientTimeout

async def main():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            metric("Bitcoin USD (live)", data["data"]["amount"])
''')
    save(13, HEADER + '''
from aiohttp import ClientSession, ClientTimeout

async def fetch(session, url):
    with span(url.split("/")[-2], "External HTTP"):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

async def main():
    urls = [f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot" for symbol in ("BTC", "ETH", "LTC")]
    async with ClientSession(timeout=ClientTimeout(total=15)) as session:
        results = await asyncio.gather(*(fetch(session, url) for url in urls))
    for data in results:
        metric(data["data"]["base"] + " USD (live)", data["data"]["amount"])
''')
    save(16, HEADER + '''
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
''')
    save(20, HEADER + '''
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
        await demo(app, [("GET", "/products/1", None, 200), ("GET", "/products/99", None, 404)])
''')
    save(18, HEADER + '''
from aiohttp import ClientSession
from api_support import server, request, object_json

async def chat(request):
    data = await object_json(request)
    prompt = data.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise web.HTTPBadRequest(text="prompt must be non-empty text")
    with span("chat", "Simulated AI wait"):
        await asyncio.sleep(3)
    return web.json_response({"response": f"Received and processed: {prompt}"})

async def status(request):
    return web.json_response({"status": "OK"})

async def main():
    app = web.Application()
    app.router.add_post("/api/v1/chat", chat)
    app.router.add_get("/api/status", status)
    async with server(app) as url:
        async with ClientSession() as client:
            chat_task = asyncio.create_task(request(client, "POST", url + "/api/v1/chat", {"prompt": "Explain await"}))
            await asyncio.sleep(0.1)
            await request(client, "GET", url + "/api/status")
            await chat_task
''')


if __name__ == '__main__':
    main()
