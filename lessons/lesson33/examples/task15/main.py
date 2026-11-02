import json

from demo_support import runtime_file
from fastapi import BackgroundTasks, FastAPI, HTTPException, Response
from lab_support import event
from pydantic import BaseModel, Field

app = FastAPI()


def append_notification(book_id):
    with runtime_file("notifications.log").open(
        "a", encoding="utf-8"
    ) as stream:
        stream.write(f"Book {book_id} created; email simulated\n")
    event("log", "background", f"Notification recorded for book {book_id}")


def update_stats(count):
    runtime_file("stats.json").write_text(
        json.dumps({"books": count}), encoding="utf-8"
    )
    event("log", "background", f"Book count recorded: {count}")


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
async def create_book(book: BookCreate, background_tasks: BackgroundTasks):
    global next_id
    record = {"id": next_id, **book.model_dump()}
    books[next_id] = record
    next_id += 1
    background_tasks.add_task(append_notification, record["id"])
    return record


@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, background_tasks: BackgroundTasks):
    if book_id not in books:
        raise HTTPException(404, "Book not found")
    del books[book_id]
    background_tasks.add_task(update_stats, len(books))
    return Response(status_code=204)
