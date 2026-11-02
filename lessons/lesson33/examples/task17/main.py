import asyncio
import json
from contextlib import asynccontextmanager

from demo_support import database_lifespan, runtime_file
from fastapi import FastAPI, Request
from lab_support import event
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def lifespan(app):
    async with database_lifespan(Base)(app):
        cache_file = runtime_file("cache.json")
        cached = (
            await asyncio.to_thread(cache_file.read_text, encoding="utf-8")
            if cache_file.exists()
            else "{}"
        )
        app.state.cache = json.loads(cached)
        event("log", "cache", "STARTUP: cache loaded")
        try:
            yield
        finally:
            await asyncio.to_thread(
                cache_file.write_text,
                json.dumps(app.state.cache),
                encoding="utf-8",
            )
            event("log", "cache", "SHUTDOWN: cache saved")


app = FastAPI(lifespan=lifespan)


@app.get("/cache")
async def get_cache(request: Request):
    return request.app.state.cache


@app.put("/cache/{key}")
async def put_cache(key: str, value: str, request: Request):
    request.app.state.cache[key] = value
    return request.app.state.cache
