from demo_support import database_lifespan, get_db
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)


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
    statement = (
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    author = (await db.execute(statement)).scalar_one_or_none()
    if author is None:
        raise HTTPException(404, "Author not found")
    return author.books
