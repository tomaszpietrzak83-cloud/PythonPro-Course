import json
import os
from urllib.request import urlopen

from fastapi import FastAPI


def join(users, posts):
    return [{**user, "posts": [post for post in posts if post["user_id"] == user["id"]]}
            for user in users]


app = FastAPI()


@app.get("/")
def home():
    role = os.environ["ROLE"]
    if role == "gateway":
        def fetch(service):
            with urlopen(f"http://{service}:8000/", timeout=5) as response:
                return json.load(response)
        return join(fetch("users-service"), fetch("posts-service"))
    import psycopg
    from psycopg.rows import dict_row
    with psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row) as db:
        if role == "users":
            db.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT)")
            db.execute("INSERT INTO users VALUES (1, 'Ada') ON CONFLICT DO NOTHING")
            return db.execute("SELECT * FROM users").fetchall()
        db.execute("CREATE TABLE IF NOT EXISTS posts (id INT PRIMARY KEY, user_id INT, title TEXT)")
        db.execute("INSERT INTO posts VALUES (1, 1, 'Hello') ON CONFLICT DO NOTHING")
        return db.execute("SELECT * FROM posts").fetchall()


def demo(work):
    result = join([{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}],
                  [{"id": 1, "user_id": 1, "title": "Hello"}])
    assert len(result[0]["posts"]) == 1 and not result[1]["posts"]
    return {"gateway": result, "databases": ["users-db", "posts-db"]}
