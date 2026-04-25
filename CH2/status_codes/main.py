import uvicorn
from fastapi import FastAPI , status
app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED) #201
async def create_item(name: str):
    return {"name": name}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)