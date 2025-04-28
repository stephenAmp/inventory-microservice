from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

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
    host='',
    port = 13982,
    password = '',
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

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
    return Product.get(pk)
    

@app.delete('/products/{pk}')
def delete(pk:str):
    return Product.delete(pk)