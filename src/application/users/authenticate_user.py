from src.application.common.auth import PasswordHasher, TokenIssuer, TokenPair, TokenStore
from src.application.common.unit_of_work import UnitOfWork
from src.application.users.dto import AuthenticateUserCommand
from src.application.users.errors import InvalidCredentialsError, TokenStorageError


class AuthenticateUserService:
    """Проверяет учётные данные и открывает пользовательскую сессию."""

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        password_hasher: PasswordHasher,
        token_issuer: TokenIssuer,
        token_store: TokenStore,
    ):
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher
        self._token_issuer = token_issuer
        self._token_store = token_store

    async def execute(self, command: AuthenticateUserCommand) -> TokenPair:
        user = await self._unit_of_work.users.get_by_email(command.email)
        if user is None or not await self._password_hasher.verify(command.password, user.hashed_password):
            raise InvalidCredentialsError('Invalid credentials')

        tokens = await self._token_issuer.issue_pair(str(user.uid))
        if not await self._token_store.save(str(user.uid), tokens.access_token):
            raise TokenStorageError('Token storage failed')

        return tokens
