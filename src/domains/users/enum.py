from src.domains.core.base_enum import BaseEnum


class UserRole(BaseEnum):
    READER = 'Reader'
    LIBRARIAN = 'Librarian'
    ADMINISTRATOR = 'Administrator'
    SUPERVISOR = 'Supervisor'
