from passlib.context import CryptContext
from pydantic.types import SecretStr

from src.settings import settings


class SecurityService:
    secret = settings.SECRET_KEY_PASSWORD.get_secret_value()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def get_hashed_password(self, password: SecretStr | str) -> str:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        return self.pwd_context.hash(password)

    def get_hashed_password_sync(self, password: SecretStr | str) -> str:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        return self.pwd_context.hash(password)
