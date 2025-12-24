import functools
import json
from typing import Callable

from redis.asyncio import Redis
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.configuration import configuration

redis: Redis  # global Redis client

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    redis = Redis(host=configuration.redis_host, port=configuration.redis_port, db=0)
    try:
        await redis.ping()
        print("Redis connected successfully")
        yield
    finally:
        await redis.close()
        await redis.connection_pool.disconnect()

def redis_cache(ttl: int = 60):
    """
    Basic async Redis cache decorator
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis = get_redis()

            # Build a simple cache key
            key_parts = [func.__module__, func.__qualname__]

            if args:
                key_parts.extend(map(str, args[1:]))  # skip `self`
            if kwargs:
                for k, v in sorted(kwargs.items()):
                    key_parts.append(f"{k}={v}")

            cache_key = "cache:" + ":".join(key_parts)

            # Try cache
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Store result
            await redis.set(
                cache_key,
                json.dumps(result, default=str),
                ex=ttl
            )

            return result

        return wrapper
    return decorator

def get_redis() -> Redis:
    return redis
