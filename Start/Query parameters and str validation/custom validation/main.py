import random
from typing import Annotated

from fastapi import FastAPI
from pydantic import AfterValidator

app = FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id_: str):
    if not id_.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id_


@app.get("/items/")
async def read_items(
    id1: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id1:
        item = data.get(id1)
    else:
        id1, item = random.choice(list(data.items()))
    return {"id": id1, "name": item}