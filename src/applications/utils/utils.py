from fastapi import Response


async def set_tokens(response: Response, tokens: dict):
    response.set_cookie(
        key='LM_user_access_token', value=tokens.get('access_token'), httponly=True, secure=True, samesite='lax'
    )

    response.set_cookie(
        key='LM_user_refresh_token', value=tokens.get('refresh_token'), httponly=True, secure=True, samesite='lax'
    )
