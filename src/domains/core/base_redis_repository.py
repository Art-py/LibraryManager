from abc import ABC

from fastapi import Depends
from redis.asyncio import Redis

from db import get_redis_client


class BaseRedisRepository(ABC):
    def __init__(self, redis_client: Redis):
        self._redis_client: Redis = redis_client

    @classmethod
    async def get_dependency(cls, redis_client: Redis = Depends(get_redis_client)):
        return cls(redis_client=redis_client)
