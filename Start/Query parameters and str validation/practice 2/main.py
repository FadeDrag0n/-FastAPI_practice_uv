from fastapi import FastAPI, Query
import uvicorn
from typing import Annotated

app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: int, username: Annotated[str, Query(min_length=2)], role: str = 'Guest'):
    return {"user_id": user_id, "username": username, "role": role}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)