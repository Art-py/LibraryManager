import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from alembic.config import Config
from alembic import command
from testcontainers.postgres import PostgresContainer

from test.core.factories.user import UserFactory
from src.repositories.users.model import User


@pytest_asyncio.fixture(scope="session")
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


@pytest_asyncio.fixture(scope="session")
async def test_engine(postgres_container):
    """Создаем асинхронный SQLAlchemy engine на контейнере."""
    url = postgres_container.get_connection_url().replace('postgresql://', 'postgresql+asyncpg://')
    engine = create_async_engine(url, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def apply_migrations(postgres_container):
    """Применяем миграции Alembic к тестовой БД."""
    config = Config('alembic.ini')
    sync_url = postgres_container.get_connection_url()
    config.set_main_option('sqlalchemy.url', sync_url)
    command.upgrade(config, 'head')
    yield


@pytest_asyncio.fixture()
async def sql_session(test_engine, apply_migrations) -> AsyncSession:
    """Создаем отдельную сессию для каждого теста."""
    async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture()
async def user_entity(sql_session):
    """Создаем пользователя через фабрику с тестовой сессией."""
    user_data = UserFactory.build().__dict__
    user_model = User(**user_data)
    sql_session.add(user_model)
    await sql_session.commit()
    await sql_session.refresh(user_model)
    return user_model
