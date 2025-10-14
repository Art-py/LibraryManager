from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

class PostgresSettings(BaseSettings):
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/environment/.env', extra='ignore')

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}'
            f'/{self.POSTGRES_DB}'
        )

class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
