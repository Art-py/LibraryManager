from fastapi import Depends
from redis.asyncio import Redis

from src.db import get_redis_client
from src.settings import RedisSettings, get_redis_settings


class BaseRedisRepository:
    def __init__(self, redis_client: Redis):
        self._redis_client: Redis = redis_client
        self._settings: RedisSettings = get_redis_settings()

    @classmethod
    async def get_dependency(cls, redis_client: Redis = Depends(get_redis_client)):
        return cls(redis_client=redis_client)
