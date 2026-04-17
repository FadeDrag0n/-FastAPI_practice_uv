from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)