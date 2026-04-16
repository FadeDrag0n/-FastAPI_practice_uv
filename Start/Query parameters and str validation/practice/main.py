from fastapi import FastAPI, Query
import uvicorn
from typing import Annotated

app = FastAPI()

@app.get("/books")
async def books(title: Annotated[str | None, Query(min_length=3)] = None, min_pages: int = 0) -> dict:
    return {"filter": title if title is not None else "no filter", "min_pages": min_pages}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)