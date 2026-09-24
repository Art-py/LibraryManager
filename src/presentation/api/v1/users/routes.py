from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from src.application.users.authenticate_user import AuthenticateUserService
from src.application.users.dto import AuthenticateUserCommand, RegisterUserCommand
from src.application.users.get_user import GetUserService
from src.application.users.register_user import RegisterUserService
from src.presentation.api.auth.cookies import set_auth_cookies
from src.presentation.api.dependencies import (
    get_authenticate_user_service,
    get_get_user_service,
    get_register_user_service,
)
from src.presentation.api.v1.users.schemas import (
    AuthenticateUserRequest,
    AuthenticationResponse,
    RegisterUserRequest,
    UserResponse,
)

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.post(
    path='/register',
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {'model': UserResponse, 'description': 'User info'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Password not confirm'},
        status.HTTP_409_CONFLICT: {'description': 'User is already registered'},
    },
)
async def register_user(
    request: RegisterUserRequest,
    service: RegisterUserService = Depends(get_register_user_service),
):
    return await service.execute(RegisterUserCommand(**request.model_dump()))


@router.post(
    path='/login',
    response_model=AuthenticationResponse,
    responses={
        status.HTTP_200_OK: {'model': AuthenticationResponse},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Invalid credentials'},
    },
)
async def authenticate_user(
    request: AuthenticateUserRequest,
    response: Response,
    service: AuthenticateUserService = Depends(get_authenticate_user_service),
):
    tokens = await service.execute(AuthenticateUserCommand(**request.model_dump()))
    set_auth_cookies(response, tokens)
    return AuthenticationResponse()


@router.get(
    path='/{user_uid}',
    response_model=UserResponse,
    responses={
        status.HTTP_200_OK: {'model': UserResponse, 'description': 'User info'},
        status.HTTP_404_NOT_FOUND: {'description': 'User not found'},
    },
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_uid: UUID,
    service: GetUserService = Depends(get_get_user_service),
):
    return await service.execute(user_uid)
