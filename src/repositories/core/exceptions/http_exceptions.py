from fastapi import status

from src.repositories.core.base_exception import BaseException


class NotFoundException(BaseException):

    def __init__(self, message: str):
        super().__init__(code=status.HTTP_404_NOT_FOUND, message=message)
