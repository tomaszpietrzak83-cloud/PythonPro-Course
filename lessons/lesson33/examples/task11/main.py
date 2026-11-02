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
