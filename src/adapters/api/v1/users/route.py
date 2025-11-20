from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from adapters.api.v1.users.schema import UserResponse
from repositories.users.repository import UserRepository

router = APIRouter(prefix='/users/{user_uid}', tags=['Пользователи'])


@router.get(path='', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def user(
    user_uid: UUID,
    repository: Annotated[UserRepository, Depends(UserRepository.get_dependency)],
):
    return await repository.get_by_uid(user_uid=user_uid)
