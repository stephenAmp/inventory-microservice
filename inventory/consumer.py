from main import redis, Product
import time

key = 'order_completed'
group = 'inventory_group'

#create consumer group
try:
    redis.xgroup_create(key, group)
except:
    print('group already exists')


#consume
while 2 > 1:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results != []:
            for result in results:
                obj: dict = result[1][0][1]    
                #fetch product from db
                try:
                    product = Product.get(obj.get('product_id'))
                    product.quantity = product.quantity - float(obj['quantity'])
                    product.save()
                except:
                    redis.xadd('refund_order',obj, '*')                        
    except Exception as e:
        print(str(e))
    time.sleep(1)