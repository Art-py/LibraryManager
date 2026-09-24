from secrets import compare_digest

from redis.asyncio import Redis


class RedisTokenStore:
    def __init__(self, redis_client: Redis, access_token_ttl_seconds: int):
        self._redis_client = redis_client
        self._access_token_ttl_seconds = access_token_ttl_seconds

    async def save(self, user_uid: str, token: str) -> bool:
        return await self._redis_client.setex(
            name=user_uid,
            time=self._access_token_ttl_seconds,
            value=token,
        )

    async def get(self, user_uid: str) -> str | None:
        token = await self._redis_client.get(user_uid)
        return token.decode() if token else None

    async def matches(self, user_uid: str, token: str) -> bool:
        stored_token = await self.get(user_uid)
        return stored_token is not None and compare_digest(stored_token, token)

    async def delete(self, user_uid: str) -> bool:
        return await self._redis_client.delete(user_uid) == 1
