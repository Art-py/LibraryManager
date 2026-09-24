from fastapi import Response

from src.application.common.auth import TokenPair


def set_auth_cookies(response: Response, tokens: TokenPair) -> None:
    response.set_cookie(
        key='LM_user_access_token',
        value=tokens.access_token,
        httponly=True,
        secure=True,
        samesite='lax',
    )
    response.set_cookie(
        key='LM_user_refresh_token',
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite='lax',
    )
