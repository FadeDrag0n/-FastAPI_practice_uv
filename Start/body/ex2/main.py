from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
import uvicorn

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)