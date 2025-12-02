from collections.abc import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import settings

engine = create_async_engine(settings.postgres.POSTGRES_ASYNC_URL, echo=settings.DEBUG)
async_session_local = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
redis_client = Redis.from_url(url=settings.redis.redis_url)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local() as session:
        yield session


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    yield redis_client
