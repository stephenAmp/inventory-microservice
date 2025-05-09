from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from settings import settings

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

class Product(HashModel):
    name: str
    price: float
    quantity: float

    class Meta:
        database = redis

@app.get("/products")
def get_all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
    product = Product.get(pk)

    return(
        {
        "id":product.pk,
        'name':product.name,
        'price': product.price,
        'quantity':product.quantity    
        }
    )

@app.post('/products')
def create(product:Product):
    return product.save()

@app.get('/products/{pk}')
def get_by_id(pk):
    try:
        product = Product.get(pk)
    except:
        raise HTTPException(status_code = 400, detail = 'product not found')
    redis.xadd('refund_order', product.model_dump(),'*')
    return product

    

@app.delete('/products/{pk}')
def delete(pk:str):
    return Product.delete(pk)