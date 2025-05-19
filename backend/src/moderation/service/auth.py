from typing import Tuple

from moderation.repository.db.user.base import AbstractUserRepository, User, UserCreate


class AuthService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    def _check_password(self, password: str, hashed_password: str) -> bool:
        return password == hashed_password
        # return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def authenticate(self, username: str, password: str) -> Tuple[bool, User | None]:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return False, None
        if not self._check_password(password, user.password_hash):
            return False, None
        return True, user

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

    def check_email_exists(self, email: str) -> bool:
        user = self.user_repository.get_by_criteria(email=email)
        return user is not None
