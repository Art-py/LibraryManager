from src.application.common.auth import PasswordHasher
from src.application.common.unit_of_work import UnitOfWork
from src.application.users.dto import RegisterUserCommand
from src.application.users.errors import PasswordMismatchError, UserAlreadyExistsError
from src.domain.users.entities import User
from src.domain.users.enums import UserRole


class RegisterUserService:
    """Регистрирует нового читателя библиотеки."""

    def __init__(self, unit_of_work: UnitOfWork, password_hasher: PasswordHasher):
        self._unit_of_work = unit_of_work
        self._password_hasher = password_hasher

    async def execute(self, command: RegisterUserCommand) -> User:
        if command.password != command.password_confirm:
            raise PasswordMismatchError('Password not confirm')

        if await self._unit_of_work.users.get_by_email(command.email) is not None:
            raise UserAlreadyExistsError('User is already registered')

        user = User(
            first_name=command.first_name,
            last_name=command.last_name,
            second_name=command.second_name,
            email=command.email,
            hashed_password=await self._password_hasher.hash(command.password),
            role=UserRole.READER,
            is_active=False,
            is_superuser=False,
            is_verified=True,
        )
        created_user = await self._unit_of_work.users.add(user)
        await self._unit_of_work.commit()
        return created_user
