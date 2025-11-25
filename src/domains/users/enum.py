from enum import StrEnum


class UserRole(StrEnum):
    READER = 'Reader'
    LIBRARIAN = 'Librarian'
    ADMINISTRATOR = 'Administrator'
    SUPERVISOR = 'Supervisor'
