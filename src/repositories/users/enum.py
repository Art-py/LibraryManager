from enum import Enum

class UserRole(str, Enum):
    READER = 'Reader'
    LIBRARIAN = 'Librarian'
    ADMINISTRATOR = 'Administrator'
    SUPERVISOR = 'Supervisor'
