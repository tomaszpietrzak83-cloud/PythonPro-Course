import hashlib
import json
import os

import requests
from celery import Celery
from fastapi import FastAPI, HTTPException
from main import recommend
from pydantic import BaseModel
from redis import Redis

REDIS = os.environ["REDIS_URL"]
celery = Celery("recommend", broker=REDIS, backend=REDIS)
app = FastAPI()


def embeddings(texts):
    response = requests.post(
        os.environ["OLLAMA_URL"] + "/api/embed",
        json={"model": "embeddinggemma", "input": texts},
        timeout=90,
    )
    response.raise_for_status()
    return response.json()["embeddings"]


@celery.task
def rank(query):
    import psycopg

    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        db.execute("CREATE TABLE IF NOT EXISTS books (title TEXT PRIMARY KEY)")
        db.execute(
            "INSERT INTO books VALUES ('Python'), ('Cooking'), ('Web services') ON CONFLICT DO NOTHING"
        )
        titles = [
            row[0]
            for row in db.execute("SELECT title FROM books ORDER BY title")
        ]
    key = (
        "rank:v1:"
        + hashlib.sha256(json.dumps([query, titles]).encode()).hexdigest()
    )
    with Redis.from_url(REDIS) as cache:
        cached = cache.get(key)
        if cached is not None:
            return json.loads(cached)
        result = recommend(query, titles, embeddings)
        cache.setex(key, 300, json.dumps(result))
    return result


class Query(BaseModel):
    text: str


@app.post("/recommendations", status_code=202)
def enqueue(query: Query):
    if not 1 <= len(query.text.strip()) <= 500:
        raise HTTPException(400, "Query must have 1–500 characters")
    return {"id": rank.delay(query.text).id}


@app.get("/recommendations/{job}")
def status(job: str):
    result = celery.AsyncResult(job)
    return {
        "state": result.state,
        "books": result.result if result.successful() else [],
    }
