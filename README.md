```python
from rcache2 import Rcache
from rcache2 import Cache as cached

...

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
redis_conn = redis.Redis(connection_pool=redis_pool)

Rcache.init(redis_conn)

fake_db = {
    '1':{'title':'Google', 'body':'...'},
    '2':{'title':'GitHub', 'body':'...'}
}

@cached
def get_item(item_id):
    time.sleep(4)
    return fake_db.get(item_id)

@app.get('/item/{item_id}')
def item(item_id):
    return get_item(item_id)

@app.put('/item/{item_id}')
def item_change(item_id, data: ItemIn):
    fake_db[item_id] = data.dict()
    get_item.cache_update(item_id).value(data.dict())
    return data

@app.delete('/item/{item_id}')
def item_create(item_id):
    del fake_db[item_id]
    get_item.cache_delete(item_id)
```