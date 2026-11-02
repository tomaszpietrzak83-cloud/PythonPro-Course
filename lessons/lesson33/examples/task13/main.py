from demo_support import database_lifespan, get_db
from fastapi import Depends, FastAPI, HTTPException, Response
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
