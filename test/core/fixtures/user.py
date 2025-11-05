import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users.model import User
from test.core.factories.user import UserFactory


@pytest_asyncio.fixture(scope='function')
async def user(
    request: pytest.FixtureRequest,
    sql_test_session: AsyncSession,
) -> User:
    """Создание пользователя"""
    param_value = getattr(request, 'param', {})
    user = UserFactory(
        **param_value,
    )
    sql_test_session.add(user)
    await sql_test_session.commit()
    return user
