"""Paginated assignments from the original tasks.md without rewriting them."""
import math
import re
from pathlib import Path

ENGLISH = ['Run three simulated asyncio.sleep operations of 1, 4 and 2 seconds concurrently using asyncio.gather. Print the total duration; it should be close to 4 seconds.', 'Build an aiohttp server whose GET / handler returns <h1>Welcome to my page!</h1> with web.Response and content_type="text/html".', 'Extend task 2 with /witaj/{name}. Read the captured name from request.match_info and return Hello, {name}!.', 'Implement GET /api/status returning JSON with status "OK" and server_time. Use datetime.now() and web.json_response().', 'Implement GET /api/search. Read q from request.query. Return the searched phrase when present; otherwise return an error indicating missing q.', 'Implement POST /api/echo. Read the request JSON with await request.json() and return the same data with web.json_response().', 'Define Product using SQLAlchemy DeclarativeBase. Include integer primary key id, name String(100), and price Integer storing cents.', 'Extend /witaj/{name} from task 3. When name equals admin, raise web.HTTPForbidden with an access-denied message.', 'Add Product from task 7 to the SQLAlchemy integration example. Include it in Base.metadata.create_all. Implement POST /products reading name and price from JSON, saving a new product, and returning its data including ID with status 201.', 'Based on task 9, implement GET /products. Retrieve all products using select(Product) and return a list of JSON objects.', 'Based on task 10, implement GET /products/{id}. Read the path ID, find the product and return JSON, or raise web.HTTPNotFound if absent. Example: select(Product).where(Product.id == product_id).', 'Write a separate client script, not a server. In main create aiohttp.ClientSession, GET https://api.coindesk.com/v1/bpi/currentprice.json, decode response.json and print Bitcoin price in USD. This old endpoint may be unavailable; use another public JSON endpoint if necessary while preserving the HTTP-client learning goal.', 'Extend task 12 with fetch(session, url). Prepare three different URLs, for example public API URLs, and use asyncio.gather to fetch all three concurrently.', 'Based on task 11, implement PUT or PATCH /products/{id}. Return 404 if absent, read new name and/or price from JSON, update attributes, save within a session and transaction, and return the updated product.', 'Based on task 11, implement DELETE /products/{id}. Retrieve the product, delete it using await session.delete(product), and return an empty response with status 204 No Content.', 'Define Account with balance: Mapped[int] and a second model as needed. Implement POST /transfer taking JSON {"from_id": 1, "to_id": 2, "amount": 100}. Within async with session.begin(), retrieve both accounts, check funds, subtract from source and add to destination. Roll back if anything fails.', 'Extend GET /products with query parameters page (default 1) and limit (default 10). Apply offset() and limit() to the SQLAlchemy query. Compute offset = (page - 1) * limit.', 'Implement POST /api/v1/chat expecting {"prompt": "some text"}. Simulate slow AI I/O using await asyncio.sleep(3), then return JSON containing a response based on the prompt. Demonstrate that other requests remain responsive.', 'Move route registration from create_app into setup_routes(app) in a separate routes.py file. Import it and call it while constructing the application.', 'Add a ForeignKey from Product to User as the product creator. Extend GET /products/{id} to return the product and creator username using select(Product, User).join(User), or options(joinedload(Product.user)).']


def assignment(number, adaptation):
    text = Path(__file__).with_name('tasks.md').read_text(encoding='utf-8')
    sections = re.split(r'^## TASK (\d+) - ', text, flags=re.MULTILINE)
    records = {int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)}
    title, body = records[number].split('\n', 1)
    return dict(source='tasks.md', title=title.strip(), adaptation=adaptation,
                pages={'pl': pages(parse_blocks(body)),
                       'en': pages(parse_blocks(ENGLISH[number - 1]))})

def parse_blocks(text):
    blocks = []
    lines = text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:]
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append({"kind": "code", "text": "\n".join(code), "language": language})
        elif re.match(r"(?:- |\d+\. )", line):
            items = []
            ordered = not line.startswith("- ")
            while i < len(lines) and re.match(r"\s*(?:- |\d+\. )", lines[i]):
                items.append(re.sub(r"^\s*(?:- |\d+\. )", "", lines[i]))
                i += 1
            blocks.append({"kind": "list", "items": items, "ordered": ordered})
            continue
        elif line.startswith("<p"):
            blocks.append({"kind": "note", "text": re.sub(r"<[^>]+>", "", line)})
        else:
            paragraph = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].lstrip().startswith(("```", "- ", "<p")):
                i += 1
                paragraph.append(lines[i].strip())
            blocks.append({"kind": "paragraph", "text": " ".join(paragraph)})
        i += 1
    return blocks


def pages(blocks):
    result, current, weight = [], [], 0
    for block in blocks:
        if block["kind"] == "code":
            size = len(block["text"].splitlines()) + 1
        elif block["kind"] == "list":
            size = sum(max(1, math.ceil(len(item) / 90)) for item in block["items"]) + 1
        else:
            size = max(1, math.ceil(len(block["text"]) / 90)) + 1
        if current and weight + size > 14:
            result.append(current)
            current, weight = [], 0
        current.append(block)
        weight += size
    if current:
        result.append(current)
    return result

