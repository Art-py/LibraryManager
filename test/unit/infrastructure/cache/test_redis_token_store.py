from unittest.mock import AsyncMock, MagicMock

import pytest
from redis.asyncio import Redis

from src.infrastructure.cache.redis_token_store import RedisTokenStore


@pytest.fixture
def redis_client() -> MagicMock:
    client = MagicMock(spec=Redis)
    client.setex = AsyncMock()
    client.get = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.fixture
def token_store(redis_client: MagicMock) -> RedisTokenStore:
    return RedisTokenStore(redis_client, access_token_ttl_seconds=300)


class TestRedisTokenStore:
    @pytest.mark.asyncio
    async def test_save_sets_access_token_ttl(self, token_store: RedisTokenStore, redis_client: MagicMock):
        redis_client.setex.return_value = True

        assert await token_store.save('user:1', 'jwt-token')
        redis_client.setex.assert_awaited_once_with(name='user:1', time=300, value='jwt-token')

    @pytest.mark.asyncio
    async def test_get_decodes_token(self, token_store: RedisTokenStore, redis_client: MagicMock):
        redis_client.get.return_value = b'jwt-token'

        assert await token_store.get('user:1') == 'jwt-token'

    @pytest.mark.asyncio
    async def test_get_returns_none_for_missing_token(self, token_store: RedisTokenStore, redis_client: MagicMock):
        redis_client.get.return_value = None

        assert await token_store.get('missing-user') is None

    @pytest.mark.asyncio
    async def test_matches_token(self, token_store: RedisTokenStore, redis_client: MagicMock):
        redis_client.get.side_effect = [b'jwt-token', b'jwt-token', None]

        assert await token_store.matches('user:1', 'jwt-token')
        assert not await token_store.matches('user:1', 'different-token')
        assert not await token_store.matches('missing-user', 'jwt-token')

    @pytest.mark.asyncio
    async def test_delete_reports_whether_token_existed(self, token_store: RedisTokenStore, redis_client: MagicMock):
        redis_client.delete.side_effect = [1, 0]

        assert await token_store.delete('user:1')
        assert not await token_store.delete('missing-user')
