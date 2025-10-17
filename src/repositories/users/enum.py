import enum


class UserRole(enum.Enum):
    READER = 'Reader'
    LIBRARIAN = 'Librarian'
    ADMINISTRATOR = 'Administrator'
    SUPERVISOR = 'Supervisor'
