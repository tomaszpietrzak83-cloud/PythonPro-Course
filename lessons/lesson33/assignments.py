"""Paginated assignments from the original tasks.md without rewriting them."""

import math
import re
from pathlib import Path

ENGLISH = [
    'Create a FastAPI app with GET / returning {"message":"Hello"}, GET /time returning current time and GET /random returning an integer 1–100. Run with uvicorn main:app --reload.',
    "Add GET /greet/{name} returning a greeting. Validate name length of at least two characters.",
    'Implement GET /calculate with a:int, b:int and operation:str="add". Support add, subtract, multiply and divide. Return an HTTP error for division by zero.',
    "Define a Pydantic Product model with name, price and quantity. POST /products accepts it and returns it with total_price = price * quantity.",
    "Use books = {} as in-memory storage. Implement GET /books, GET /books/{id}, POST /books and DELETE /books/{id}.",
    "Extend task 5 with 201 Created for creation, 204 No Content for deletion and 404 Not Found for an absent book.",
    "Define User with email: EmailStr. POST /users validates the email address.",
    "Add title, description, version, endpoint tags and docstrings with examples. Inspect /docs.",
    "Split the book app into main.py, routers/books.py and routers/authors.py. Use APIRouter and include_router.",
    "Create verify_api_key dependency checking the X-API-Key header. Use it in three endpoints.",
    "Define Author(name,email) and Book(title,author:Author,price). POST /books accepts nested JSON.",
    "Define Product with validators: name contains only letters/digits; price is greater than 0 and no more than 10000; category is Electronics, Books or Clothing. With Pydantic v2 use field_validator.",
    "Convert the book API to async SQLAlchemy. Include Book ORM, input/output Pydantic schemas, a database-session dependency and complete CRUD.",
    "Add a one-to-many Author → Books relationship and GET /authors/{id}/books. Use eager loading such as selectinload.",
    "Extend the book API with BackgroundTasks: after creating a book write an email/log notification to a file; after deletion update statistics.",
    "Add middleware logging request method/path and duration, adding X-Request-ID, and saving entries to requests.log.",
    "At startup initialize the database and read cache from a JSON file. On shutdown save cache and close database connections. Prefer lifespan in new FastAPI projects.",
    "Extend GET /books with skip, limit, category, min_price, max_price and sort_by (for example price/title).",
    "Build a Mini Blog API: user CRUD, post CRUD, author-only editing, post comments, GET /posts/{id}/with-comments, eager loading for comments, and a background email notification for new comments.",
    "Extend Blog API: POST /posts/{id}/summarize through OpenAI or simulation; background sentiment analysis; middleware detecting profanity/disallowed content. Local simulation is sufficient for the architecture exercise.",
]


def assignment(number, adaptation):
    text = Path(__file__).with_name("tasks.md").read_text(encoding="utf-8")
    sections = re.split(r"^## TASK (\d+) - ", text, flags=re.MULTILINE)
    records = {
        int(sections[i]): sections[i + 1] for i in range(1, len(sections), 2)
    }
    title, body = records[number].split("\n", 1)
    return dict(
        source="tasks.md",
        title=title.strip(),
        adaptation=adaptation,
        pages={
            "pl": pages(parse_blocks(body)),
            "en": pages(parse_blocks(ENGLISH[number - 1])),
        },
    )


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
            blocks.append({
                "kind": "code",
                "text": "\n".join(code),
                "language": language,
            })
        elif re.match(r"(?:- |\d+\. )", line):
            items = []
            ordered = not line.startswith("- ")
            while i < len(lines) and re.match(r"\s*(?:- |\d+\. )", lines[i]):
                items.append(re.sub(r"^\s*(?:- |\d+\. )", "", lines[i]))
                i += 1
            blocks.append({"kind": "list", "items": items, "ordered": ordered})
            continue
        elif line.startswith("<p"):
            blocks.append({
                "kind": "note",
                "text": re.sub(r"<[^>]+>", "", line),
            })
        else:
            paragraph = [line]
            while (
                i + 1 < len(lines)
                and lines[i + 1].strip()
                and not lines[i + 1].lstrip().startswith(("```", "- ", "<p"))
            ):
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
            size = (
                sum(
                    max(1, math.ceil(len(item) / 90)) for item in block["items"]
                )
                + 1
            )
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
