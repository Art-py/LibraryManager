from fastapi import APIRouter

from .users.route import router as user_route

routers = APIRouter(
    prefix='/v1',
)

routers.include_router(user_route)

__all__ = [
    'routers',
]
