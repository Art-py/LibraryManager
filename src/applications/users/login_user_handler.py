from fastapi import Depends, Response

from src.applications.utils.utils import set_tokens
from src.domains.auth.token_repository import TokenRepository
from src.domains.users.exception import InvalidPassword, TokenStoreError, UserNotFound
from src.domains.users.schema import UserLogin
from src.domains.users.security import create_tokens, verify_password
from src.domains.users.uow import UserUOW


class LoginUserHandler:
    """Хэндлер для логина пользователя"""

    def __init__(self, unit: UserUOW, token_repository: TokenRepository):
        self.unit = unit
        self.token_repository = token_repository
        self.repository = self.unit.get_user_repository()

    @classmethod
    async def get_dependency(
        cls,
        unit: UserUOW = Depends(UserUOW.get_dependency),
        token_repository: TokenRepository = Depends(TokenRepository.get_dependency),
    ):
        return cls(unit=unit, token_repository=token_repository)

    async def handle(self, user_data: UserLogin, response: Response) -> dict:
        user = await self.repository.get_by_email(user_email=user_data.email)
        if user is None:
            raise UserNotFound('Invalid credentials')

        if not await verify_password(user_data.password, user.hashed_password):
            raise InvalidPassword('Invalid credentials')

        tokens = await create_tokens(str(user.uid))
        if not await self.token_repository.add(user_uid=str(user.uid), data=tokens.get('access_token')):
            raise TokenStoreError('Token storage failed')

        await set_tokens(response, tokens)

        return tokens
