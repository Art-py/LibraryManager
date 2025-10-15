from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class CoreBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'{BASE_DIR}/environment/.env', extra='ignore'
    )


class PostgresSettings(CoreBaseSettings):
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 5432

    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )

    @property
    def POSTGRES_SYNC_URL(self) -> str:
        return (
            f'postgresql+psycopg2://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )


class Settings(CoreBaseSettings):
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
