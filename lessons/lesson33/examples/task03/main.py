from typing import Literal

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/calculate")
async def calculate(
    a: int,
    b: int,
    operation: Literal["add", "subtract", "multiply", "divide"] = "add",
):
    if operation == "divide" and b == 0:
        raise HTTPException(400, "Cannot divide by zero")
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    else:
        result = a / b
    return {"result": result}
