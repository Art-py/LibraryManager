import asyncio
from asyncio import to_thread
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import AsyncRedisContainer

from alembic import command
from src.db import get_async_session, get_redis_client
from src.main import app

# Инициализация фикстур
pytest_plugins = [
    'test.core.fixtures.user',
]


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def postgres_container():
    """
    Поднимаем временный Postgres контейнер на всю тестовую сессию
    """
    container = PostgresContainer(image='postgres:17-alpine', driver='asyncpg')
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest_asyncio.fixture(scope='session')
async def async_redis_container():
    """Поднятие redis контейнера для тестов"""

    async_container = AsyncRedisContainer('redis:8')
    async_container.start()
    try:
        yield async_container
    finally:
        async_container.stop()


@pytest_asyncio.fixture(scope='session')
async def apply_migrations(postgres_container):
    """Применяем миграции Alembic к тестовой БД"""
    config = Config('alembic.ini')
    async_url = postgres_container.get_connection_url()
    config.set_main_option('sqlalchemy.url', async_url)
    await to_thread(command.upgrade, config, 'head')
    yield


@pytest_asyncio.fixture()
async def test_engine(postgres_container):
    """Создаем асинхронный SQLAlchemy engine на контейнере"""
    async_url = postgres_container.get_connection_url()
    engine = create_async_engine(async_url, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def test_redis_client(async_redis_container) -> AsyncGenerator[Redis, None]:
    async_client = await async_redis_container.get_async_client()

    await async_client.flushdb(asynchronous=True)
    yield async_client
    await async_client.aclose()


@pytest_asyncio.fixture()
async def sql_test_session(test_engine, apply_migrations) -> AsyncGenerator[AsyncSession, None]:
    """Создаем отдельную сессию для каждого теста"""
    async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture()
async def override_get_db_fixture(sql_test_session: AsyncSession):
    async def override_get_db():
        yield sql_test_session

    app.dependency_overrides[get_async_session] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def override_get_redis_fixture(test_redis_client):
    async def override_get_redis():
        yield test_redis_client

    app.dependency_overrides[get_redis_client] = override_get_redis
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def client(override_get_db_fixture, override_get_redis_fixture):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac
