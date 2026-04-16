from fastapi import FastAPI
import uvicorn
import pydantic

app = FastAPI()

class Book(pydantic.BaseModel):
    title: str
    pages: int
    price: float = 0.0


@app.post("/books/{book_id}")
async def create_book(book_id: int, book: Book):
    return {"id": book_id, **book.model_dump()}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)