from enum import Enum
from urllib.request import Request

from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import Field
app = FastAPI()
import pydantic


class Category(str, Enum):
    pc = 'PC'
    laptop = 'Laptop'
    Phone = 'Phone'
    console = 'Console'


class Product(pydantic.BaseModel):
    name: str = pydantic.Field(max_length=15, default="Product Name")
    category: Category
    price: float = pydantic.Field(gt=0, default=100, lt=99999)
    description: str | None = pydantic.Field(max_length=2500, default=None)


product_list = []

@app.post("/products", summary="Create new product", tags=["Products"])
async def post_product(product: Product) -> dict:
    product_list.append({'id': 1 if not product_list else (product_list[-1]['id']+1), **product.model_dump()})
    return {'success': True}

@app.get("/products", tags=["Products"], summary="List all products")
async def get_products() -> dict[str, list[dict]]:
    return {'products': product_list}

@app.get("/products/{id}", tags=["Products"], summary="Get a product")
async def get_product(id_: int):
    for item in product_list:
        if item['id'] == id_:
            return item
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{id}", tags=["Products"], summary="Update a product")
async def update_product(id_: int, product: Product) -> dict:
    for index, item in enumerate(product_list):
        if item['id'] == id_:
            product_list[index] = {'id': id_, **product.model_dump()}
            return {'Success': True}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{id}", tags=["Products"], summary="Delete a product")
async def delete_product(id_: int) -> dict:
    for index, item in enumerate(product_list):
        if item['id'] == id_:
            del product_list[index]
            return {'Success': True}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/", tags=["Products"], summary="Delete all products in category")
async def delete_products_by_category(category: Category) -> dict:
    global product_list
    to_remove = [item for item in product_list if item['category'] == category.value]
    product_list = [item for item in product_list if item not in to_remove]
    return {'Success': True}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)