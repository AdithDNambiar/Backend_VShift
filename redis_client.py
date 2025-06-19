import os
import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

def store_token(key, value):
    r.set(key, value)

def get_token(key):
    return r.get(key)
