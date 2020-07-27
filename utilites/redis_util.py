import aioredis

from contextlib import asynccontextmanager
from typing import AsyncContextManager


Redis = aioredis.Redis


@asynccontextmanager
async def create_redis_pool() -> AsyncContextManager[Redis]:
    redis = await aioredis.create_redis_pool('redis://localhost')
    try:
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()
