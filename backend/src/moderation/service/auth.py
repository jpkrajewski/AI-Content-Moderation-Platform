import logging
from typing import Tuple

from moderation.repository.db.user.base import AbstractUserRepository, User, UserCreate

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    def _check_password(self, password: str, hashed_password: str) -> bool:
        return password == hashed_password
        # return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate(self, email: str, password: str) -> Tuple[bool, User | None]:
        hash_password = self.user_repository.get_password_hash_by_email(email)
        if not hash_password:
            return False, None
        if not self._check_password(hash_password, password):
            print("failed password check")
            return False, None
        return True, self.user_repository.get_by_criteria(email=email)

    def register(self, username: str, password: str, email: str) -> Tuple[bool, User | None]:
        user = self.user_repository.get_by_criteria(email=email)
        if user:
            return False, None
        user = UserCreate(
            email=email,
            username=username,
            password_hash=password,
            role="moderator",
        )
        return True, self.user_repository.save_user(user)
