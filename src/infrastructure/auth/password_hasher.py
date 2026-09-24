from passlib.context import CryptContext
from pydantic import SecretStr

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class BcryptPasswordHasher:
    async def hash(self, password: str) -> str:
        return self.hash_sync(password)

    async def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.verify_sync(plain_password, hashed_password)

    @staticmethod
    def hash_sync(password: SecretStr | str) -> str:
        raw_password = password.get_secret_value() if isinstance(password, SecretStr) else password
        return password_context.hash(raw_password)

    @staticmethod
    def verify_sync(plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)
