import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from moderation.core.settings import settings


class JwtTokenHandler:
    def __init__(self) -> None:
        self.secret = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM

    def generate_token(self, user_id: str, scopes: list[str], expires_in_minutes: int | None = None) -> str:
        now = datetime.now(timezone.utc)
        expiration = now + timedelta(minutes=expires_in_minutes or settings.JWT_EXPIRATION_ACCESS)

        payload = {
            "jti": str(uuid.uuid4()),
            "iat": int(now.timestamp()),
            "exp": int(expiration.timestamp()),
            "user_id": user_id,
            "scopes": scopes,
        }

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def generate_access_refresh_pair(self,
        user_id: str,
        scopes: list[str],
    ) -> tuple[str, str]:
        access = self.generate_token(user_id=user_id, scopes=scopes, expires_in_minutes=settings.JWT_EXPIRATION_ACCESS)
        refresh = self.generate_token(user_id=user_id, scopes=[], expires_in_minutes=settings.JWT_EXPIRATION_REFRESH)
        return access, refresh

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("JWT has expired")
        except jwt.InvalidTokenError as exc:
            raise jwt.InvalidTokenError(f"JWT validation failed: {exc}")

    def validate_token(self, token: str) -> bool:
        self.decode_token(token)  # Let it raise if invalid
        return True
