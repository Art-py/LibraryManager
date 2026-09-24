from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENVIRONMENT_DIR = Path(__file__).resolve().parents[3] / 'environment'


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENVIRONMENT_DIR / '.env', extra='ignore')


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENVIRONMENT_DIR / '.env.postgresql', extra='ignore')

    postgres_user: str = ''
    postgres_password: SecretStr = SecretStr('')
    postgres_db: str = ''
    postgres_host: str = ''
    postgres_port: int = 5432

    @property
    def async_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_user}'
            f':{self.postgres_password.get_secret_value()}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )

    @property
    def sync_url(self) -> str:
        return (
            f'postgresql+psycopg2://{self.postgres_user}'
            f':{self.postgres_password.get_secret_value()}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENVIRONMENT_DIR / '.env.redis', extra='ignore')

    redis_user: str = ''
    redis_user_password: SecretStr = SecretStr('')
    redis_host: str = ''
    redis_port: int = 6379
    jwt_cache_db: int = Field(default=0, validation_alias=AliasChoices('JWT_CACHE_DB', 'BD_JWT_CASH'))

    @property
    def url(self) -> str:
        return (
            f'redis://{self.redis_user}:{self.redis_user_password.get_secret_value()}'
            f'@{self.redis_host}:{self.redis_port}/{self.jwt_cache_db}'
        )


class AdminUserSettings(EnvironmentSettings):
    user_admin_email: str = ''
    user_admin_password: SecretStr = SecretStr('')


class AuthSettings(EnvironmentSettings):
    jwt_secret: SecretStr = SecretStr('(O.o)')
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 1


class MainSettings(EnvironmentSettings):
    debug: bool = True


@lru_cache
def get_main_settings() -> MainSettings:
    return MainSettings()


@lru_cache
def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()


@lru_cache
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


@lru_cache
def get_admin_user_settings() -> AdminUserSettings:
    return AdminUserSettings()


@lru_cache
def get_auth_settings() -> AuthSettings:
    return AuthSettings()
