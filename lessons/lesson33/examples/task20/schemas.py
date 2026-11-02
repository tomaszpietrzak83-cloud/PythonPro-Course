from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = Field(min_length=1, max_length=5000)


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=1000)
