from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class Product(BaseModel):
    name: str
    price: float = Field(gt=0, le=10000)
    category: Literal["Electronics", "Books", "Clothing"]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.isalnum():
            raise ValueError("Use letters and digits only")
        return value


@app.post("/products")
async def create_product(product: Product):
    return product
