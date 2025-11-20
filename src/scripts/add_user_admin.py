import asyncio

from db import async_session_local
from src.repositories.users.enum import UserRole
from src.repositories.users.model import User
from src.repositories.users.security import SecurityService
from src.settings import settings

security_service = SecurityService()


async def create_user_admin():
    """
    Генерирует пользователя с администраторским доступом,
    записывает его в БД, логин и пароль берет из .env
    """

    async with async_session_local() as session:
        reg_data = {
            'first_name': 'Admin',
            'last_name': 'Admin',
            'email': settings.user_admin.USER_ADMIN_EMAIL,
            'hashed_password': await security_service.get_hashed_password(
                password=settings.user_admin.USER_ADMIN_PASSWORD
            ),
            'role': UserRole.ADMINISTRATOR,
            'is_active': True,
            'is_superuser': True,
            'is_verified': True,
        }

        user = User(**reg_data)
        session.add(user)

        try:
            await session.commit()
        except Exception:
            return 'User was created...'

        return 'User admin has been added...'


if __name__ == '__main__':
    print(asyncio.run(create_user_admin()))
