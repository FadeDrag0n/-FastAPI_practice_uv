from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

#1. База

class User(BaseModel):
    username: str
    age: int

users = [
    User(username="john", age=30), User(username='Jane', age=15)]


@app.get("/users/{user_id}", summary="Get user details", tags=["Task 1"])
async def get_user(user_id: int, check_age: bool = False):
    if check_age:
        if users[user_id].age >= 18:
            return users[user_id]
        else:
            return {"message": "User age is below 18"}
    else:
        return users[user_id]


#2. Фильтрация

class Goods(BaseModel):
    title: str
    description: str
    price: float

goods_list = [
    Goods(title="Laptop", description="High performance laptop", price=1200),
    Goods(title="Smartphone", description="Latest model smartphone", price=900),
    Goods(title="Headphones", description="Noise cancelling headphones", price=150),
    Goods(title="Keyboard", description="Mechanical keyboard", price=100),
    Goods(title="Mouse", description="Wireless mouse", price=50),
    Goods(title="Monitor", description="4K monitor", price=400),
    Goods(title="Printer", description="Laser printer", price=250),
    Goods(title="Camera", description="Digital SLR camera", price=800),
    Goods(title="Watch", description="Smart watch", price=200),
    Goods(title="Tablet", description="10-inch tablet", price=600),
    Goods(title="Speaker", description="Bluetooth speaker", price=120),
    Goods(title="Backpack", description="Durable travel backpack", price=80),
    Goods(title="Lamp", description="LED desk lamp", price=40),
    Goods(title="Chair", description="Ergonomic office chair", price=300),
    Goods(title="Desk", description="Wooden office desk", price=350),
    Goods(title="Flash Drive", description="128GB USB drive", price=25),
    Goods(title="Hard Drive", description="2TB external hard drive", price=100),
    Goods(title="Microphone", description="Studio quality microphone", price=180),
    Goods(title="Webcam", description="HD webcam", price=70),
    Goods(title="Gamepad", description="Wireless game controller", price=60)
]

@app.get("/goods", tags=["Task 2"], summary="Get goods filtered by price")
async def get_goods(min_price: float = 0, max_price: float = max([item.price for item in goods_list])):
    res = []
    for item in goods_list:
        if min_price <= item.price <= max_price:
            res.append(item)
    return res

#3. Комбинированное

posts = [{'user_id': 1, 'post_id': 1, 'text': 'blablabla'}, {'user_id': 1, 'post_id': 2, 'text': 'blablabla'}, {'user_id': 2, 'post_id': 3, 'text': 'blablabla'}, {'user_id': 3, 'post_id': 4, 'text': 'blablabla'}, {'user_id': 1, 'post_id': 5, 'text': 'blablabla'}]

@app.get("users/{user_id}/posts", tags=["Task 3"], summary="Get posts with lims by user")
async def get_posts(user_id: int, limit: int | None = None):
    user_posts = [post for post in posts if post['user_id'] == user_id]
    if not limit:
        return user_posts
    return user_posts[:limit]


# 4. Ловушка 🔥

users2 = [{'id': 1, 'name': 'Artem'}, {'id': 2, 'name': 'Volodymyr'}, {'id': 3, 'name': 'Kate'}]

@app.get('/users2/', tags=["Task 4"], summary="Get user by id or name")
async def get_user(user_id: int | None = None, user_name: str | None = None) -> dict:
    for user in users2:
        if user_id is None and user_name is None:
            raise HTTPException(400, "Provide user_id or user_name")
        if user_id is not None and user['id'] == user_id:
            return user
        if user_name is not None and user['name'] == user_name:
            return user
    raise HTTPException(status_code=404, detail='User not found')

# 5. Чуть сложнее

class Status(str, Enum):
    pending = 'Pending'
    confirmed = 'Confirmed'
    shipped = 'Shipped'
    transit = 'Transit'
    delivered = 'Delivered'
    cancelled = 'Cancelled'
    refunded = 'Refunded'

orders = [{'order_id': 1, 'user_id': 1, 'price': 2500, 'status': 'Pending'}, {'order_id': 2, 'user_id': 1, 'price': 500, 'status': 'Delivered'}, {'order_id': 3, 'user_id': 1, 'price': 1700, 'status': 'Pending'},{'order_id': 4, 'user_id': 2, 'price': 5500, 'status': 'Refunded'}, {'order_id': 5, 'user_id': 2, 'price': 2500, 'status': 'Pending'}]

@app.get('/orders/{us_id}', tags=["Task 5"], summary="Get order by user with filter")
async def get_orders(us_id: int, status: Status | None = None, sort_by_price: bool = False) -> list[dict]:
    if sort_by_price:
        user_orders = sorted([order for order in orders if order['user_id'] == us_id], key=lambda order: order['price'])
    else:
        user_orders = [order for order in orders if order['user_id'] == us_id]
    if not status:
        return user_orders
    else:
        return [order for order in user_orders if order['status'] == status.value]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
