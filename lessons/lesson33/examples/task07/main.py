from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class User(BaseModel):
    email: EmailStr


@app.post("/users")
async def create_user(user: User):
    return user
