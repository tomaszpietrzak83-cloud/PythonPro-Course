import random
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/time")
async def current_time():
    return {"time": datetime.now(timezone.utc).isoformat()}


@app.get("/random")
async def random_number():
    return {"number": random.randint(1, 100)}
