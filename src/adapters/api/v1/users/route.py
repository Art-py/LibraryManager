from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.adapters.api.v1.users.schema import UserResponse
from src.repositories.users.repository import UserRepository

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get(
    path='/{user_uid}',
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {
            'model': UserResponse,
            'description': 'User info',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'User not found',
        },
    },
    status_code=status.HTTP_200_OK,
)
async def user(
    user_uid: UUID,
    repository: Annotated[UserRepository, Depends(UserRepository.get_dependency)],
):
    return await repository.get_by_uid(user_uid=user_uid)
