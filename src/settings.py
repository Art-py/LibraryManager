from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class CoreBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/environment/.env', extra='ignore')


class PostgresSettings(CoreBaseSettings):
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: SecretStr = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 5432

    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD.get_secret_value()}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )

    @property
    def POSTGRES_SYNC_URL(self) -> str:
        return (
            f'postgresql+psycopg2://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD.get_secret_value()}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )


class UserAdminSettings(CoreBaseSettings):
    USER_ADMIN_EMAIL: str = ''
    USER_ADMIN_PASSWORD: SecretStr = ''


class PasswordSettings(CoreBaseSettings):
    JWT_SECRET: SecretStr = '(O.o)'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1


class Settings(CoreBaseSettings):
    DEBUG: bool = True

    postgres: PostgresSettings = PostgresSettings()
    user_admin: UserAdminSettings = UserAdminSettings()
    password_settings: PasswordSettings = PasswordSettings()


settings = Settings()
