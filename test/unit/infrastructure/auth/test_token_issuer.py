import pytest
from jose import jwt
from pydantic import SecretStr

from src.infrastructure.auth.token_issuer import JwtTokenIssuer
from src.infrastructure.config.settings import AuthSettings


@pytest.mark.asyncio
async def test_issues_typed_access_and_refresh_tokens():
    settings = AuthSettings(jwt_secret=SecretStr('test-secret'), jwt_algorithm='HS256')
    issuer = JwtTokenIssuer(settings)

    tokens = await issuer.issue_pair('user-id')
    access_payload = jwt.decode(tokens.access_token, 'test-secret', algorithms=['HS256'])
    refresh_payload = jwt.decode(tokens.refresh_token, 'test-secret', algorithms=['HS256'])

    assert access_payload['sub'] == 'user-id'
    assert access_payload['type'] == 'access'
    assert refresh_payload['sub'] == 'user-id'
    assert refresh_payload['type'] == 'refresh'
    assert tokens.access_token != tokens.refresh_token
