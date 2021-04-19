"""Utils for redis connection."""
import aioredis

from contextlib import asynccontextmanager
from typing import AsyncContextManager


Redis = aioredis.Redis


@asynccontextmanager
async def create_redis_pool() -> AsyncContextManager[Redis]:
    """Create redis poll as as async content manager."""
    redis = await aioredis.create_redis_pool(f'redis://chill_redis')
    try:
        yield redis
    finally:
        redis.close()
        await redis.wait_closed()
