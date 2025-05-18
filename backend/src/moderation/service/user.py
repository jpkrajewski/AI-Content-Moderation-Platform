from moderation.repository.db.user.base import AbstractUserRepository


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    def exists(self, username: str) -> bool:
        """Check if a user exists in the database."""
        return self.user_repository.get_user_by_username(username) is not None

    def create_user(self, user_data: dict) -> bool:
        """Create a new user in the database."""
        return self.user_repository.save_user(user_data["id"], user_data)
