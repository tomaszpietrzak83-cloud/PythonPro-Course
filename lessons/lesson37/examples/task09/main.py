import json
import os
from fastapi import FastAPI


def lookup(key, read, write):
    cached = read(key)
    if cached is not None:
        return {"source": "cache", "value": json.loads(cached)}
    value = {"id": key, "title": "Python"}
    write(key, json.dumps(value))
    return {"source": "database", "value": value}


app = FastAPI()


@app.get("/items/{key}")
def item(key: str):
    from redis import Redis
    with Redis.from_url(os.environ["REDIS_URL"]) as client:
        return lookup(key, client.get, lambda k, v: client.setex(k, 60, v))


def demo(work):
    cache = {}
    results = [lookup("book", cache.get, cache.__setitem__) for _ in range(2)]
    assert [item["source"] for item in results] == ["database", "cache"]
    return {"adapter": "local dictionary", "reads": results}
