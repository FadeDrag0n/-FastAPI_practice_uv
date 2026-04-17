from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/items2/{item_id}")
async def read_items2(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)