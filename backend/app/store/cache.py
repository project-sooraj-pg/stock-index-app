import redis.asyncio as redis

from backend.app.core.configuration import configuration

redis_client = redis.from_url(configuration.redis_url, decode_responses=True)

async def get_cache():
    return redis_client