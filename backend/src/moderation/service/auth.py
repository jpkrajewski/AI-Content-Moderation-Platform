import logging
from typing import Optional, Tuple

import bcrypt
from moderation.repository.db.user.base import AbstractUserRepository, User, UserCreate

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    @staticmethod
    def _check_password(password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception as e:
            logger.exception(f"Password check failed: {e}")
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def authenticate(self, email: str, password: str) -> Tuple[bool, Optional[User]]:
        user = self.user_repository.get_by_criteria(email=email)
        if not user:
            logger.info(f"Authentication failed: no user found for email {email}")
            return False, None
        if not self._check_password(password, user.hashed_password):
            logger.info(f"Authentication failed: invalid password for email {email}")
            return False, None
        return True, user

    def register(
        self, username: str, password: str, email: str, role: str = "moderator", external: bool = False, profile_picture_url: str | None = None
    ) -> Tuple[bool, Optional[User]]:
        existing_user = self.user_repository.get_by_criteria(email=email)
        if existing_user:
            logger.info(f"Registration failed: user already exists for email {email}")
            return False, None

        user = UserCreate(
            email=email,
            username=username,
            password_hash=self.hash_password(password),
            role=role,
            profile_picture_url=profile_picture_url,
            external=external,
        )
        created_user = self.user_repository.save_user(user)
        return True, created_user
