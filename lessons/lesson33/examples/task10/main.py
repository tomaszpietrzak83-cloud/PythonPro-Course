import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key is None or not secrets.compare_digest(
        x_api_key, "lesson-demo-key"
    ):
        raise HTTPException(401, "Invalid API key")
    return x_api_key


@app.get("/books", dependencies=[Depends(verify_api_key)])
async def list_books():
    return {"books": []}


@app.get("/authors", dependencies=[Depends(verify_api_key)])
async def list_authors():
    return {"authors": []}


@app.get("/stats", dependencies=[Depends(verify_api_key)])
async def stats():
    return {"count": 0}
