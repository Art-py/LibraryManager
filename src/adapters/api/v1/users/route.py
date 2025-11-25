from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.applications.users.create_user_handler import CreateUserHandler
from src.domains.users.repository import UserRepository
from src.domains.users.schema import UserCreate, UserResponse

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.post(
    path='/register',
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {
            'model': UserResponse,
            'description': 'User info',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Password not confirm',
        },
        status.HTTP_409_CONFLICT: {
            'description': 'User is already registered',
        },
    },
)
async def user_register(
    user_data: UserCreate,
    handler: CreateUserHandler = Depends(CreateUserHandler.get_dependency),
):
    return await handler.handle(user_data)


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
async def user_get_by_uid(
    user_uid: UUID,
    repository: UserRepository = Depends(UserRepository.get_dependency),
):
    return await repository.get_by_uid(user_uid=user_uid)
