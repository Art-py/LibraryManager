from factory import Factory, LazyFunction
from factory.fuzzy import FuzzyChoice
from faker import Faker
from pydantic import SecretStr

from src.repositories.users.enum import UserRole
from src.repositories.users.model import User
from src.repositories.users.security import SecurityService

security_service = SecurityService()


faker = Faker(locale='ru')


class UserFactory(Factory):
    """Фабрика пользователя"""

    first_name = LazyFunction(lambda: faker.first_name())
    last_name = LazyFunction(lambda: faker.last_name())

    email = LazyFunction(lambda: faker.email())
    hashed_password = LazyFunction(
        lambda: security_service.get_hashed_password_sync(SecretStr(faker.password(length=10)))
    )

    role = FuzzyChoice([role.value for role in UserRole])

    is_active = LazyFunction(lambda: faker.boolean())
    is_superuser = LazyFunction(lambda: faker.boolean())
    is_verified = LazyFunction(lambda: faker.boolean())

    class Meta:
        model = User
