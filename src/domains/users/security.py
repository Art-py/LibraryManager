from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic.types import SecretStr

from src.settings import get_password_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_hashed_password(password: SecretStr | str) -> str:
    """Получить хэш пароля"""
    if isinstance(password, SecretStr):
        password = password.get_secret_value()
    return pwd_context.hash(password)


def get_hashed_password_sync(password: SecretStr | str) -> str:
    """Получить хэш пароля"""
    if isinstance(password, SecretStr):
        password = password.get_secret_value()
    return pwd_context.hash(password)


async def create_access_token(data: dict, date: datetime) -> str:
    """Создает access токен"""
    password_settings = get_password_settings()
    access_expire = date + timedelta(minutes=password_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_payload = data.copy()
    access_payload.update({'exp': int(access_expire.timestamp()), 'type': 'access'})
    return jwt.encode(
        access_payload,
        password_settings.JWT_SECRET.get_secret_value(),
        algorithm=password_settings.JWT_ALGORITHM,
    )


async def create_refresh_token(data: dict, date: datetime) -> str:
    """Создает refresh токен"""
    password_settings = get_password_settings()
    refresh_expire = date + timedelta(days=password_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_payload = data.copy()
    refresh_payload.update({'exp': int(refresh_expire.timestamp()), 'type': 'refresh'})
    return jwt.encode(
        refresh_payload,
        password_settings.JWT_SECRET.get_secret_value(),
        algorithm=password_settings.JWT_ALGORITHM,
    )


async def create_tokens(user_uid: str) -> dict:
    """
    Создание пары токенов access и refresh
    """
    now = datetime.now(UTC)
    data = {'sub': user_uid}
    return {
        'access_token': await create_access_token(data, now),
        'refresh_token': await create_refresh_token(data, now),
    }


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)
