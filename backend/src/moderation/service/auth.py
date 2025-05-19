from dataclasses import dataclass
from uuid import UUID

import jwt
from moderation.core.settings import settings
from moderation.repository.db.user.base import AbstractUserRepository


@dataclass
class JwtUser:
    uuid: UUID
    roles: list

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "roles": self.roles,
        }


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    def _check_password(self, password: str, hashed_password: str) -> bool:
        return password == hashed_password
        # return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise ValueError("User not found")
        if not self._check_password(password, ""):
            raise ValueError("Invalid password")
        return user

    def generate_jwt_token(self, user_id: str) -> str:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return jwt.encode({"user_id": user_id, "roles": user.roles}, settings.JWT_SECRET, algorithm="HS256")

    def decode_jwt_token(self, token: str) -> JwtUser:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return JwtUser(uuid=UUID(payload["user_id"]), roles=payload.get("roles", []))
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def verify_token(self, token: str, required_scopes: list) -> JwtUser:
        user = self.decode_jwt_token(token)
        result = all(scope in user.roles for scope in required_scopes)
        if not result:
            raise ValueError("Insufficient permissions")
        return user
