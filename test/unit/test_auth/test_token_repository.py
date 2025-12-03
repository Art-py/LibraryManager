import pytest
import pytest_asyncio
from redis.asyncio import Redis

from src.domains.auth.token_repository import TokenRepository


@pytest_asyncio.fixture
async def token_repository(test_redis_client: Redis) -> TokenRepository:
    """Создание экземпляра TokenRepository"""
    return TokenRepository(redis_client=test_redis_client)


class TestTokenRepository:
    @pytest.mark.asyncio
    async def test_add_value_success(
        self,
        token_repository: TokenRepository,
        test_redis_client: Redis,
    ):
        key = 'user:1'
        val = 'jwt_token'

        assert await token_repository.add(key, val)
        assert await test_redis_client.get(key) == val.encode()

        ttl = await test_redis_client.ttl(key)
        assert ttl > 0
        assert ttl <= token_repository._settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    @pytest.mark.asyncio
    async def test_exist_value_success(
        self,
        token_repository: TokenRepository,
    ):
        key = 'user:2'
        val = 'jwt_token'

        assert await token_repository.add(key, val)
        assert await token_repository.exist(key)

    @pytest.mark.asyncio
    async def test_exist_value_failure(
        self,
        token_repository: TokenRepository,
    ):
        key = 'user:2'
        val = 'jwt_token'

        assert await token_repository.add(key, val)
        assert await token_repository.exist(key)
        assert not await token_repository.exist('user:1')

    @pytest.mark.asyncio
    async def test_delete_value_success(
        self,
        token_repository: TokenRepository,
    ):
        key = 'user:2'
        val = 'jwt_token'

        assert await token_repository.add(key, val)
        assert await token_repository.delete(key)

    @pytest.mark.asyncio
    async def test_delete_value_failure(
        self,
        token_repository: TokenRepository,
    ):
        key = 'user:2'

        assert not await token_repository.delete(key)

    @pytest.mark.asyncio
    async def test_overwrite_value(
        self,
        token_repository: TokenRepository,
        test_redis_client: Redis,
    ):
        key = 'user:1'
        val = 'jwt_token'
        new_val = 'jwt_token_new'

        assert await token_repository.add(key, val)
        assert await token_repository.add(key, new_val)
        result = await test_redis_client.get(key)
        assert result.decode('utf-8') == new_val
