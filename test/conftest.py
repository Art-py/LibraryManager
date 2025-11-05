from asyncio import to_thread

import pytest_asyncio
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from alembic import command

# Инициализация фикстур
pytest_plugins = [
    'test.core.fixtures.user',
]


@pytest_asyncio.fixture(scope='session')
async def postgres_container():
    """
    Поднимаем временный Postgres контейнер на всю тестовую сессию
    """
    container = PostgresContainer('postgres:17-alpine')
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest_asyncio.fixture(scope='function')
async def test_engine(postgres_container):
    """Создаем асинхронный SQLAlchemy engine на контейнере"""
    url = postgres_container.get_connection_url().replace('postgresql+psycopg2', 'postgresql+asyncpg')
    engine = create_async_engine(url, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def apply_migrations(postgres_container):
    """Применяем миграции Alembic к тестовой БД"""
    config = Config('alembic.ini')
    async_url = postgres_container.get_connection_url().replace('postgresql+psycopg2', 'postgresql+asyncpg')
    config.set_main_option('sqlalchemy.url', async_url)
    await to_thread(command.upgrade, config, 'head')
    yield


@pytest_asyncio.fixture(scope='function')
async def sql_test_session(test_engine, apply_migrations) -> AsyncSession:
    """Создаем отдельную сессию для каждого теста"""
    async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.rollback()
