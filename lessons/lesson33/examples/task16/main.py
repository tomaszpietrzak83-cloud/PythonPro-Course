import asyncio
import json
import time
import uuid

from demo_support import runtime_file
from fastapi import FastAPI, Request

app = FastAPI()
log_lock = asyncio.Lock()


@app.middleware("http")
async def log_request(request: Request, call_next):
    request_id = uuid.uuid4().hex
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    entry = {
        "method": request.method,
        "path": request.url.path,
        "seconds": time.perf_counter() - started,
        "request_id": request_id,
    }
    async with log_lock:
        await asyncio.to_thread(append_log, entry)
    return response


def append_log(entry):
    with runtime_file("requests.log").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry) + "\n")


@app.get("/books")
async def list_books():
    return {"books": []}
