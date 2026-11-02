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
