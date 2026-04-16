from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)