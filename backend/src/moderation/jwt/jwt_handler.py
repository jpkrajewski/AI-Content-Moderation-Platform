import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from moderation.core.settings import settings


class JwtTokenHandler:
    def __init__(self) -> None:
        self.secret = settings.JWT_SECRET
        self.algorithm = settings.JWT_ALGORITHM

    def generate_token(self, user_id: str, scopes: list[str], expires_in_minutes: int = 30) -> str:
        now = datetime.now(timezone.utc)
        expiration = now + timedelta(minutes=expires_in_minutes)

        payload = {
            "jti": str(uuid.uuid4()),
            "iat": int(now.timestamp()),
            "exp": int(expiration.timestamp()),
            "user_id": user_id,
            "scopes": scopes,
        }

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

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
