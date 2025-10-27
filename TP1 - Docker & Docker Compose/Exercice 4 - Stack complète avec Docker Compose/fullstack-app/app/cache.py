import redis
import os

def get_redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "cache"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )
