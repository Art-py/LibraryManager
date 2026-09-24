from datetime import UTC, datetime, timedelta

from jose import jwt

from src.application.common.auth import TokenPair
from src.infrastructure.config.settings import AuthSettings


class JwtTokenIssuer:
    def __init__(self, settings: AuthSettings):
        self._settings = settings

    async def issue_pair(self, user_uid: str) -> TokenPair:
        now = datetime.now(UTC)
        return TokenPair(
            access_token=self._encode(
                user_uid=user_uid,
                expires_at=now + timedelta(minutes=self._settings.access_token_expire_minutes),
                token_type='access',
            ),
            refresh_token=self._encode(
                user_uid=user_uid,
                expires_at=now + timedelta(days=self._settings.refresh_token_expire_days),
                token_type='refresh',
            ),
        )

    def _encode(self, user_uid: str, expires_at: datetime, token_type: str) -> str:
        payload = {'sub': user_uid, 'exp': int(expires_at.timestamp()), 'type': token_type}
        return jwt.encode(
            payload,
            self._settings.jwt_secret.get_secret_value(),
            algorithm=self._settings.jwt_algorithm,
        )
