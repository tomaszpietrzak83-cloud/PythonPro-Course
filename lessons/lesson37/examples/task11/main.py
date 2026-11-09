import os
import sqlite3
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Book(BaseModel):
    title: str


@contextmanager
def connection():
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        import psycopg
        with psycopg.connect(dsn) as db:
            yield db, "%s"
    else:
        db = sqlite3.connect(os.environ["LOCAL_DB"])
        try:
            with db:
                yield db, "?"
        finally:
            db.close()


def init(db):
    db.execute("CREATE TABLE IF NOT EXISTS books (id BIGINT PRIMARY KEY, title TEXT NOT NULL)")


app = FastAPI()


@app.get("/books")
def list_books():
    with connection() as (db, p):
        init(db)
        return [{"id": key, "title": title} for key, title in
                db.execute("SELECT id, title FROM books ORDER BY id").fetchall()]


@app.post("/books", status_code=201)
def add_book(book: Book):
    from secrets import randbits
    key = randbits(52)
    with connection() as (db, p):
        init(db)
        db.execute(f"INSERT INTO books VALUES ({p}, {p})", (key, book.title))
    return {"id": key, "title": book.title}


@app.put("/books/{key}")
def update_book(key: int, book: Book):
    with connection() as (db, p):
        init(db)
        result = db.execute(f"UPDATE books SET title={p} WHERE id={p}", (book.title, key))
        if not result.rowcount:
            raise HTTPException(404, "Book not found")
    return {"id": key, "title": book.title}


@app.delete("/books/{key}", status_code=204)
def delete_book(key: int):
    with connection() as (db, p):
        init(db)
        result = db.execute(f"DELETE FROM books WHERE id={p}", (key,))
        if not result.rowcount:
            raise HTTPException(404, "Book not found")


def demo(work):
    from unittest.mock import patch
    from fastapi.testclient import TestClient

    with patch.dict(os.environ, {"DATABASE_URL": "", "LOCAL_DB": str(work / "books.sqlite3")}):
        client = TestClient(app)
        created = client.post("/books", json={"title": "Python"})
        key = created.json()["id"]
        updated = client.put(f"/books/{key}", json={"title": "Docker"})
        listed = client.get("/books")
        removed = client.delete(f"/books/{key}")
        missing = client.put(f"/books/{key}", json={"title": "Again"})
        statuses = [r.status_code for r in (created, updated, listed, removed, missing)]
        assert statuses == [201, 200, 200, 204, 404]
        assert listed.json()[0]["title"] == "Docker"
    from pathlib import Path
    root = Path(__file__).parent
    assert "proxy_pass http://backend:8000" in (root / "nginx.conf").read_text()
    assert (root / "static/index.html").is_file()
    return {"database": "local SQLite", "statuses": statuses, "before_delete": listed.json()}
