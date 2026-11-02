from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


@app.post("/products")
async def product_total(product: Product):
    return {
        **product.model_dump(),
        "total_price": product.price * product.quantity,
    }
