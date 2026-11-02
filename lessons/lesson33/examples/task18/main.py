from demo_support import database_lifespan, get_db
from fastapi import Depends, FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str | None = None,
    min_price: int = Query(0, ge=0),
    max_price: int | None = Query(None, ge=0),
    sort_by: str = "price",
    db: AsyncSession = Depends(get_db),
):
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
    return result.scalars().all()


@app.get("/books/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if book is None:
        raise HTTPException(404, "Book not found")
    return book


@app.put("/books/{book_id}", response_model=BookRead)
async def replace_book(
    book_id: int, data: BookCreate, db: AsyncSession = Depends(get_db)
):
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
