import jwt
from moderation.core.settings import settings


class JwtTokenHandler:

    def generate_token(self, user_id: str, scopes: list[str]) -> str:
        return jwt.encode(
            {"user_id": user_id, "scopes": scopes},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except Exception:
            return {}

    def validate_token(self, token: str) -> bool:
        try:
            self.decode_token(token)
            return True
        except ValueError:
            return False
