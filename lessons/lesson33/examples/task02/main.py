from typing import Annotated

from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/greet/{name}")
async def greet(name: Annotated[str, Path(min_length=2)]):
    return {"message": f"Hello, {name}!"}
