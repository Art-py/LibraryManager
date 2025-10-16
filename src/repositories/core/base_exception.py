from abc import ABC

from fastapi import HTTPException


class BaseHTTPException(ABC, HTTPException):
    """Базовый класс для всех эксепшенов"""

    def __init__(self, code: int, message: str):
        super().__init__(status_code=code, detail=message)
