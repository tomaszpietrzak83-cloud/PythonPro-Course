"""Authoring source: independent FastAPI exercises. Running this overwrites examples."""

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent / "examples"


def write(n, source, name="main.py"):
    target = ROOT / f"task{n:02}" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(source).strip() + "\n", encoding="utf-8")


COMMON = """
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI()
books = {}
next_id = 1

class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    price: float = Field(gt=0)

@app.get("/books")
async def list_books():
    return list(books.values())

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(404, "Book not found")
    return books[book_id]

@app.post("/books", status_code=201)
async def create_book(book: BookCreate):
    global next_id
    record = {"id": next_id, **book.model_dump()}
    books[next_id] = record
    next_id += 1
    return record

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(404, "Book not found")
    del books[book_id]
    return Response(status_code=204)
"""

DB = """
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from demo_support import database_lifespan, get_db

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(40), default="Books")

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    price: int = Field(gt=0, le=1000000)
    category: str = Field(default="Books", max_length=40)

class BookRead(BookCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

app = FastAPI(lifespan=database_lifespan(Base))

@app.post("/books", response_model=BookRead, status_code=201)
async def create_book(data: BookCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        book = Book(**data.model_dump())
        db.add(book)
        await db.flush()
    return book

@app.get("/books", response_model=list[BookRead])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).order_by(Book.id))
    return result.scalars().all()

@app.get("/books/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(404, "Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookRead)
async def replace_book(book_id: int, data: BookCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        book = await db.get(Book, book_id)
        if book is None:
            raise HTTPException(404, "Book not found")
        book.title = data.title
        book.price = data.price
        book.category = data.category
    return book

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        book = await db.get(Book, book_id)
        if book is None:
            raise HTTPException(404, "Book not found")
        await db.delete(book)
    return Response(status_code=204)
"""


def main():
    write(
        1,
        """
    import random
    from datetime import datetime, timezone
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello"}

    @app.get("/time")
    async def current_time():
        return {"time": datetime.now(timezone.utc).isoformat()}

    @app.get("/random")
    async def random_number():
        return {"number": random.randint(1, 100)}
    """,
    )
    write(
        2,
        """
    from typing import Annotated
    from fastapi import FastAPI, Path

    app = FastAPI()

    @app.get("/greet/{name}")
    async def greet(name: Annotated[str, Path(min_length=2)]):
        return {"message": f"Hello, {name}!"}
    """,
    )
    write(
        3,
        """
    from typing import Literal
    from fastapi import FastAPI, HTTPException

    app = FastAPI()

    @app.get("/calculate")
    async def calculate(a: int, b: int, operation: Literal["add", "subtract", "multiply", "divide"] = "add"):
        if operation == "divide" and b == 0:
            raise HTTPException(400, "Cannot divide by zero")
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        else:
            result = a / b
        return {"result": result}
    """,
    )
    write(
        4,
        """
    from fastapi import FastAPI
    from pydantic import BaseModel, Field

    app = FastAPI()

    class Product(BaseModel):
        name: str = Field(min_length=1)
        price: float = Field(gt=0)
        quantity: int = Field(gt=0)

    @app.post("/products")
    async def product_total(product: Product):
        return {**product.model_dump(), "total_price": product.price * product.quantity}
    """,
    )
    write(
        5,
        COMMON
        .replace(", status_code=201", "")
        .replace(", status_code=204", "")
        .replace(
            "return Response(status_code=204)", 'return {"deleted": book_id}'
        ),
    )
    write(6, COMMON)
    write(
        7,
        """
    from fastapi import FastAPI
    from pydantic import BaseModel, EmailStr

    app = FastAPI()

    class User(BaseModel):
        email: EmailStr

    @app.post("/users")
    async def create_user(user: User):
        return user
    """,
    )
    write(
        8,
        '''
    from fastapi import FastAPI
    from pydantic import BaseModel, Field

    app = FastAPI(title="Book Workshop", description="An educational book API", version="1.0.0")

    class Book(BaseModel):
        title: str = Field(examples=["Python Basics"])

    @app.post("/books", response_model=Book, tags=["books"], summary="Create a book")
    async def create_book(book: Book):
        """Accept a title, for example Python Basics, and echo validated data."""
        return book
    ''',
    )
    write(
        9,
        """
    from fastapi import FastAPI
    from routers import authors, books

    app = FastAPI()
    app.include_router(books.router)
    app.include_router(authors.router)
    """,
    )
    write(9, "", "routers/__init__.py")
    write(
        9,
        COMMON
        .replace("FastAPI, HTTPException", "APIRouter, HTTPException")
        .replace(
            "app = FastAPI()",
            'router = APIRouter(prefix="/books", tags=["books"])',
        )
        .replace("@app.", "@router.")
        .replace('"/books/{book_id}"', '"/{book_id}"')
        .replace('"/books"', '""'),
        "routers/books.py",
    )
    # The prefix remains /books; only decorator paths lose the common prefix.
    path = ROOT / "task09/routers/books.py"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            'prefix=""', 'prefix="/books"'
        ),
        encoding="utf-8",
    )
    write(
        9,
        """
    from fastapi import APIRouter

    router = APIRouter(prefix="/authors", tags=["authors"])

    @router.get("")
    async def list_authors():
        return [{"id": 1, "name": "Anna"}]
    """,
        "routers/authors.py",
    )
    write(
        10,
        """
    import secrets
    from typing import Annotated
    from fastapi import Depends, FastAPI, Header, HTTPException

    app = FastAPI()

    async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
        if x_api_key is None or not secrets.compare_digest(x_api_key, "lesson-demo-key"):
            raise HTTPException(401, "Invalid API key")
        return x_api_key

    @app.get("/books", dependencies=[Depends(verify_api_key)])
    async def list_books():
        return {"books": []}

    @app.get("/authors", dependencies=[Depends(verify_api_key)])
    async def list_authors():
        return {"authors": []}

    @app.get("/stats", dependencies=[Depends(verify_api_key)])
    async def stats():
        return {"count": 0}
    """,
    )
    write(
        11,
        """
    from fastapi import FastAPI
    from pydantic import BaseModel, EmailStr, Field

    app = FastAPI()

    class Author(BaseModel):
        name: str = Field(min_length=2)
        email: EmailStr

    class Book(BaseModel):
        title: str = Field(min_length=1)
        author: Author
        price: float = Field(gt=0)

    @app.post("/books")
    async def create_book(book: Book):
        return book
    """,
    )
    write(
        12,
        """
    from typing import Literal
    from fastapi import FastAPI
    from pydantic import BaseModel, Field, field_validator

    app = FastAPI()

    class Product(BaseModel):
        name: str
        price: float = Field(gt=0, le=10000)
        category: Literal["Electronics", "Books", "Clothing"]

        @field_validator("name")
        @classmethod
        def validate_name(cls, value):
            if not value.isalnum():
                raise ValueError("Use letters and digits only")
            return value

    @app.post("/products")
    async def create_product(product: Product):
        return product
    """,
    )
    write(
        15,
        COMMON
        .replace(
            "from fastapi import FastAPI,",
            "import json\nfrom fastapi import BackgroundTasks, FastAPI,",
        )
        .replace(
            "app = FastAPI()",
            """from demo_support import runtime_file
from lab_support import event

app = FastAPI()

def append_notification(book_id):
    with runtime_file("notifications.log").open("a", encoding="utf-8") as stream:
        stream.write(f"Book {book_id} created; email simulated\\n")
    event("log", "background", f"Notification recorded for book {book_id}")

def update_stats(count):
    runtime_file("stats.json").write_text(json.dumps({"books": count}), encoding="utf-8")
    event("log", "background", f"Book count recorded: {count}")
""",
        )
        .replace(
            "async def create_book(book: BookCreate):",
            "async def create_book(book: BookCreate, background_tasks: BackgroundTasks):",
        )
        .replace(
            "    return record",
            '    background_tasks.add_task(append_notification, record["id"])\n    return record',
        )
        .replace(
            "async def delete_book(book_id: int):",
            "async def delete_book(book_id: int, background_tasks: BackgroundTasks):",
        )
        .replace(
            "    del books[book_id]",
            "    del books[book_id]\n    background_tasks.add_task(update_stats, len(books))",
        ),
    )
    write(
        16,
        """
    import asyncio
    import json
    import time
    import uuid
    from fastapi import FastAPI, Request
    from demo_support import runtime_file

    app = FastAPI()
    log_lock = asyncio.Lock()

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        request_id = uuid.uuid4().hex
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        entry = {"method": request.method, "path": request.url.path, "seconds": time.perf_counter() - started, "request_id": request_id}
        async with log_lock:
            await asyncio.to_thread(append_log, entry)
        return response

    def append_log(entry):
        with runtime_file("requests.log").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry) + "\\n")

    @app.get("/books")
    async def list_books():
        return {"books": []}
    """,
    )
    write(
        17,
        """
    import asyncio
    import json
    from contextlib import asynccontextmanager
    from fastapi import FastAPI, Request
    from sqlalchemy.orm import DeclarativeBase
    from demo_support import database_lifespan, runtime_file
    from lab_support import event

    class Base(DeclarativeBase):
        pass

    @asynccontextmanager
    async def lifespan(app):
        async with database_lifespan(Base)(app):
            cache_file = runtime_file("cache.json")
            cached = await asyncio.to_thread(cache_file.read_text, encoding="utf-8") if cache_file.exists() else "{}"
            app.state.cache = json.loads(cached)
            event("log", "cache", "STARTUP: cache loaded")
            try:
                yield
            finally:
                await asyncio.to_thread(cache_file.write_text, json.dumps(app.state.cache), encoding="utf-8")
                event("log", "cache", "SHUTDOWN: cache saved")

    app = FastAPI(lifespan=lifespan)

    @app.get("/cache")
    async def get_cache(request: Request):
        return request.app.state.cache

    @app.put("/cache/{key}")
    async def put_cache(key: str, value: str, request: Request):
        request.app.state.cache[key] = value
        return request.app.state.cache
    """,
    )
    write(13, DB)
    paginated = DB.replace("Depends, FastAPI,", "Depends, FastAPI, Query,")
    old = """async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).order_by(Book.id))
    return result.scalars().all()"""
    new = """async def list_books(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), category: str | None = None, min_price: int = Query(0, ge=0), max_price: int | None = Query(None, ge=0), sort_by: str = "price", db: AsyncSession = Depends(get_db)):
    if max_price is not None and min_price > max_price:
        raise HTTPException(400, "Invalid price range")
    if sort_by not in {"price", "title"}:
        raise HTTPException(400, "Unknown sort field")
    statement = select(Book).where(Book.price >= min_price)
    if max_price is not None:
        statement = statement.where(Book.price <= max_price)
    if category is not None:
        statement = statement.where(Book.category == category)
    order = Book.price if sort_by == "price" else Book.title
    statement = statement.order_by(order, Book.id).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.scalars().all()"""
    write(18, paginated.replace(old, new))
    write(
        14,
        """
    from fastapi import Depends, FastAPI, HTTPException
    from pydantic import BaseModel, ConfigDict, Field
    from sqlalchemy import ForeignKey, Integer, String, select
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload
    from demo_support import database_lifespan, get_db

    class Base(DeclarativeBase):
        pass

    class Author(Base):
        __tablename__ = "authors"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(100))
        books: Mapped[list["Book"]] = relationship(back_populates="author")

    class Book(Base):
        __tablename__ = "books"
        id: Mapped[int] = mapped_column(primary_key=True)
        title: Mapped[str] = mapped_column(String(100))
        author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
        author: Mapped[Author] = relationship(back_populates="books")

    class BookRead(BaseModel):
        model_config = ConfigDict(from_attributes=True)
        id: int
        title: str

    class AuthorCreate(BaseModel):
        name: str = Field(min_length=1, max_length=100)

    class BookCreate(BaseModel):
        title: str = Field(min_length=1, max_length=100)
        author_id: int

    app = FastAPI(lifespan=database_lifespan(Base))

    @app.post("/authors", status_code=201)
    async def create_author(data: AuthorCreate, db: AsyncSession = Depends(get_db)):
        async with db.begin():
            author = Author(**data.model_dump())
            db.add(author)
            await db.flush()
        return {"id": author.id, "name": author.name}

    @app.post("/books", status_code=201)
    async def create_book(data: BookCreate, db: AsyncSession = Depends(get_db)):
        async with db.begin():
            if await db.get(Author, data.author_id) is None:
                raise HTTPException(404, "Author not found")
            book = Book(**data.model_dump())
            db.add(book)
            await db.flush()
        return {"id": book.id, "title": book.title}

    @app.get("/authors/{author_id}/books", response_model=list[BookRead])
    async def author_books(author_id: int, db: AsyncSession = Depends(get_db)):
        statement = select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
        author = (await db.execute(statement)).scalar_one_or_none()
        if author is None:
            raise HTTPException(404, "Author not found")
        return author.books
    """,
    )
    build_blog(19)
    build_blog(20)


def build_blog(number):
    write(
        number,
        """
    from sqlalchemy import ForeignKey, String
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(50), unique=True)

    class Post(Base):
        __tablename__ = "posts"
        id: Mapped[int] = mapped_column(primary_key=True)
        title: Mapped[str] = mapped_column(String(100))
        body: Mapped[str] = mapped_column(String(5000))
        user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
        comments: Mapped[list["Comment"]] = relationship(back_populates="post", passive_deletes=True)

    class Comment(Base):
        __tablename__ = "comments"
        id: Mapped[int] = mapped_column(primary_key=True)
        body: Mapped[str] = mapped_column(String(1000))
        user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
        post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
        post: Mapped[Post] = relationship(back_populates="comments")
    """,
        "models.py",
    )
    write(
        number,
        """
    from pydantic import BaseModel, Field

    class UserCreate(BaseModel):
        name: str = Field(min_length=2, max_length=50)

    class PostCreate(BaseModel):
        title: str = Field(min_length=1, max_length=100)
        body: str = Field(min_length=1, max_length=5000)

    class CommentCreate(BaseModel):
        body: str = Field(min_length=1, max_length=1000)
    """,
        "schemas.py",
    )
    write(
        number,
        """
    from typing import Annotated
    from fastapi import Header, HTTPException, Request
    from sqlalchemy import select
    from models import User

    DEMO_KEYS = {"demo-anna-key": 1, "demo-jan-key": 2}

    async def get_actor(request: Request, x_api_key: Annotated[str | None, Header()] = None):
        user_id = DEMO_KEYS.get(x_api_key)
        if user_id is None:
            raise HTTPException(401, "Use a demonstration API key")
        async with request.app.state.sessions() as session:
            user = await session.get(User, user_id)
            if user is None:
                raise HTTPException(401, "Demo user does not exist")
            return user.id
    """,
        "auth.py",
    )
    write(number, "", "routers/__init__.py")
    write(
        number,
        """
    from fastapi import APIRouter, Depends, HTTPException, Response
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from auth import get_actor
    from demo_support import get_db
    from models import User
    from schemas import UserCreate

    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("", status_code=201)
    async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
        async with db.begin():
            user = User(**data.model_dump())
            db.add(user)
            await db.flush()
        return {"id": user.id, "name": user.name}

    @router.get("")
    async def list_users(db: AsyncSession = Depends(get_db)):
        users = (await db.execute(select(User).order_by(User.id))).scalars().all()
        return [{"id": user.id, "name": user.name} for user in users]

    @router.get("/{user_id}")
    async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(404, "User not found")
        return {"id": user.id, "name": user.name}

    @router.put("/{user_id}")
    async def replace_user(user_id: int, data: UserCreate, actor: int = Depends(get_actor), db: AsyncSession = Depends(get_db)):
        if actor != user_id:
            raise HTTPException(403, "Only the account owner may edit")
        async with db.begin():
            user = await db.get(User, user_id)
            user.name = data.name
        return {"id": user.id, "name": user.name}

    @router.delete("/{user_id}", status_code=204)
    async def delete_user(user_id: int, actor: int = Depends(get_actor), db: AsyncSession = Depends(get_db)):
        if actor != user_id:
            raise HTTPException(403, "Only the account owner may delete")
        async with db.begin():
            user = await db.get(User, user_id)
            await db.delete(user)
        return Response(status_code=204)
    """,
        "routers/users.py",
    )
    write(
        number,
        """
    import json
    from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import selectinload
    from auth import get_actor
    from demo_support import get_db, runtime_file
    from lab_support import event
    from models import Comment, Post
    from schemas import CommentCreate, PostCreate

    router = APIRouter(prefix="/posts", tags=["posts"])

    def post_data(post):
        return {"id": post.id, "title": post.title, "body": post.body, "user_id": post.user_id}

    def notify_author(post_id):
        with runtime_file("email.log").open("a", encoding="utf-8") as stream:
            stream.write(f"New comment on post {post_id}; email simulated\\n")
        event("log", "background", "Author notification recorded")

    @router.post("", status_code=201)
    async def create_post(data: PostCreate, actor: int = Depends(get_actor), db: AsyncSession = Depends(get_db)):
        async with db.begin():
            post = Post(**data.model_dump(), user_id=actor)
            db.add(post)
            await db.flush()
        return post_data(post)

    @router.get("")
    async def list_posts(db: AsyncSession = Depends(get_db)):
        posts = (await db.execute(select(Post).order_by(Post.id))).scalars().all()
        return [post_data(post) for post in posts]

    @router.get("/{post_id}")
    async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
        post = await db.get(Post, post_id)
        if post is None:
            raise HTTPException(404, "Post not found")
        return post_data(post)

    @router.put("/{post_id}")
    async def replace_post(post_id: int, data: PostCreate, actor: int = Depends(get_actor), db: AsyncSession = Depends(get_db)):
        async with db.begin():
            post = await db.get(Post, post_id)
            if post is None:
                raise HTTPException(404, "Post not found")
            if post.user_id != actor:
                raise HTTPException(403, "Only the author may edit")
            post.title = data.title
            post.body = data.body
        return post_data(post)

    @router.delete("/{post_id}", status_code=204)
    async def delete_post(post_id: int, actor: int = Depends(get_actor), db: AsyncSession = Depends(get_db)):
        async with db.begin():
            post = await db.get(Post, post_id)
            if post is None:
                raise HTTPException(404, "Post not found")
            if post.user_id != actor:
                raise HTTPException(403, "Only the author may delete")
            await db.delete(post)
        return Response(status_code=204)

    @router.post("/{post_id}/comments", status_code=201)
    async def add_comment(post_id: int, data: CommentCreate, background_tasks: BackgroundTasks, actor: int = Depends(get_actor), db: AsyncSession = Depends(get_db)):
        async with db.begin():
            if await db.get(Post, post_id) is None:
                raise HTTPException(404, "Post not found")
            comment = Comment(body=data.body, post_id=post_id, user_id=actor)
            db.add(comment)
            await db.flush()
        background_tasks.add_task(notify_author, post_id)
        return {"id": comment.id, "body": comment.body}

    @router.get("/{post_id}/with-comments")
    async def post_with_comments(post_id: int, db: AsyncSession = Depends(get_db)):
        statement = select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)
        post = (await db.execute(statement)).scalar_one_or_none()
        if post is None:
            raise HTTPException(404, "Post not found")
        return {**post_data(post), "comments": [{"id": c.id, "body": c.body} for c in post.comments]}
    """,
        "routers/posts.py",
    )
    write(
        number,
        """
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    from sqlalchemy.exc import IntegrityError
    from demo_support import database_lifespan
    from models import Base
    from routers import posts, users

    app = FastAPI(lifespan=database_lifespan(Base), title="Mini Blog API")
    app.include_router(users.router)
    app.include_router(posts.router)

    @app.exception_handler(IntegrityError)
    async def conflict(request: Request, error: IntegrityError):
        return JSONResponse({"detail": "Conflicting data"}, status_code=409)
    """,
    )
    if number == 20:
        build_ai(number)


def build_ai(number):
    target = ROOT / f"task{number:02}" / "routers/posts.py"
    source = target.read_text(encoding="utf-8")
    source = source.replace(
        "def notify_author(post_id):",
        """def analyze_sentiment(comment_id, body):
    sentiment = "positive" if "great" in body.lower() else "negative" if "bad" in body.lower() else "neutral"
    with runtime_file("sentiment.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"comment_id": comment_id, "sentiment": sentiment, "mode": "rule-based simulation"}) + "\\n")
    event("log", "background", f"Simulated sentiment: {sentiment}")

def notify_author(post_id):""",
    )
    source = source.replace(
        "background_tasks.add_task(notify_author, post_id)",
        "background_tasks.add_task(notify_author, post_id)\n    background_tasks.add_task(analyze_sentiment, comment.id, comment.body)",
    )
    source += """

@router.post("/{post_id}/summarize")
async def summarize(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if post is None:
        raise HTTPException(404, "Post not found")
    summary = " ".join(post.body.split()[:12])
    return {"summary": summary, "mode": "local simulation, not a language model"}
"""
    target.write_text(source, encoding="utf-8")
    target = ROOT / f"task{number:02}" / "main.py"
    source = target.read_text(encoding="utf-8")
    source += """

@app.middleware("http")
async def moderate(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH"}:
        body = await request.body()
        if len(body) > 64000:
            return JSONResponse({"detail": "Body too large"}, status_code=413)
        if b"forbiddenword" in body.lower():
            return JSONResponse({"detail": "Demo moderation rejected content"}, status_code=400)
    return await call_next(request)
"""
    target.write_text(source, encoding="utf-8")


if __name__ == "__main__":
    main()
