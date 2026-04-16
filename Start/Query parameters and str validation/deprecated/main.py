# Маркировка параметров как устаревших¶
#
# Предположим, этот параметр вам больше не нравится.
#
# Его нужно оставить на какое‑то время, так как клиенты его используют, но вы хотите, чтобы в документации он явно отображался как устаревший.
#
# Тогда передайте параметр deprecated=True в Query:


from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)