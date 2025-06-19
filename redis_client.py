import redis

# Connect to local Redis server
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def store_token(key, value):
    r.set(key, value)

def get_token(key):
    return r.get(key)

def delete_token(key):
    r.delete(key)
