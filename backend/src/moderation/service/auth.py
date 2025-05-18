from moderation.repository.db.user.base import AbstractUserRepository


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
