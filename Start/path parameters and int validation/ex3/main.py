from typing import Annotated
import uvicorn
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: Annotated[int, Query(ge=555, le=1000)]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)