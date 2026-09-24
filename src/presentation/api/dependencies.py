from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.users.authenticate_user import AuthenticateUserService
from src.application.users.get_user import GetUserService
from src.application.users.register_user import RegisterUserService
from src.infrastructure.auth.password_hasher import BcryptPasswordHasher
from src.infrastructure.auth.token_issuer import JwtTokenIssuer
from src.infrastructure.cache.client import get_redis_client
from src.infrastructure.cache.redis_token_store import RedisTokenStore
from src.infrastructure.config.settings import AuthSettings, get_auth_settings
from src.infrastructure.database.session import get_async_session
from src.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork


def get_unit_of_work(session: AsyncSession = Depends(get_async_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


def get_token_issuer(settings: AuthSettings = Depends(get_auth_settings)) -> JwtTokenIssuer:
    return JwtTokenIssuer(settings)


def get_token_store(
    redis_client: Redis = Depends(get_redis_client),
    settings: AuthSettings = Depends(get_auth_settings),
) -> RedisTokenStore:
    return RedisTokenStore(
        redis_client=redis_client,
        access_token_ttl_seconds=settings.access_token_expire_minutes * 60,
    )


def get_register_user_service(
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
) -> RegisterUserService:
    return RegisterUserService(unit_of_work, password_hasher)


def get_authenticate_user_service(
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    token_issuer: JwtTokenIssuer = Depends(get_token_issuer),
    token_store: RedisTokenStore = Depends(get_token_store),
) -> AuthenticateUserService:
    return AuthenticateUserService(unit_of_work, password_hasher, token_issuer, token_store)


def get_get_user_service(
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> GetUserService:
    return GetUserService(unit_of_work)
