from fastapi import status

from src.domains.core.base_exception import BaseException


class InvalidPassword(BaseException):
    def __init__(self, message: str):
        super().__init__(code=status.HTTP_401_UNAUTHORIZED, message=message)


class UserNotFound(BaseException):
    def __init__(self, message: str):
        super().__init__(code=status.HTTP_401_UNAUTHORIZED, message=message)


class UserIsRegistered(BaseException):
    def __init__(self, message: str):
        super().__init__(code=status.HTTP_409_CONFLICT, message=message)


class PasswordRequired(BaseException):
    def __init__(self, message: str):
        super().__init__(code=status.HTTP_400_BAD_REQUEST, message=message)


class TokenStoreError(BaseException):
    def __init__(self, message: str):
        super().__init__(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message)
