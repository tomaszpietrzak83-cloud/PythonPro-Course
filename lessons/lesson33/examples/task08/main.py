from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Book Workshop",
    description="An educational book API",
    version="1.0.0",
)


class Book(BaseModel):
    title: str = Field(examples=["Python Basics"])


@app.post(
    "/books", response_model=Book, tags=["books"], summary="Create a book"
)
async def create_book(book: Book):
    """Accept a title, for example Python Basics, and echo validated data."""
    return book
