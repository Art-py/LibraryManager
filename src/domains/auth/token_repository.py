from src.domains.core.base_redis_repository import BaseRedisRepository


class TokenRepository(BaseRedisRepository):
    """Репозиторий для управления кэшированием jwt токенов"""

    async def add(self, user_uid: str, data: str) -> bool:
        return await self._redis_client.setex(
            name=user_uid, time=self._settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, value=data
        )

    async def exist(self, user_uid: str) -> bool:
        return await self._redis_client.exists(user_uid) == 1

    async def delete(self, user_uid: str) -> bool:
        return await self._redis_client.delete(user_uid) == 1
