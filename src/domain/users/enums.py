from enum import StrEnum


class UserRole(StrEnum):
    READER = 'Reader'
    LIBRARIAN = 'Librarian'
    ADMINISTRATOR = 'Administrator'
    SUPERVISOR = 'Supervisor'

    @classmethod
    def values(cls) -> list[str]:
        return [role.value for role in cls]
