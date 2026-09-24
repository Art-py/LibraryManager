from collections.abc import AsyncGenerator

from redis.asyncio import Redis

from src.infrastructure.config.settings import get_redis_settings

redis_client = Redis.from_url(url=get_redis_settings().url)


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    yield redis_client
