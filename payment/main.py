from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from settings import settings
from starlette.requests import Request
import httpx
from fastapi.background import BackgroundTasks
import time

app = FastAPI()

url = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = url,
    allow_credentials=True,
    allow_methods = ['*'],
    allow_headers=["*"]
)


redis = get_redis_connection(
    host= settings.DB_HOST,
    port = settings.DB_PORT,
    password = settings.DB_PASSWORD,
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    quantity: float
    cost_price: float
    fee: float
    selling_price:float
    status: str

    class Meta:
        database = redis


@app.get('/orders/{pk}')
async def get_by_id(pk:str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, background_tasks:BackgroundTasks):
    body = await request.json()

    with httpx.Client(timeout=5) as client:
        response = client.get('http://localhost:8000/products/%s' % body['id'])
    product = response.json()

    order = Order(
        product_id = body['id'],
        cost_price = product['price'],
        fee = 0.2 * product['price'],
        selling_price = 1.2 * product['price'],
        quantity = body['quantity'],
        status = 'draft'
    )

    order.save()
    background_tasks.add_task(status_completed, order)
    return order
    
def status_completed(order:Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
        
