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

    def get_user(self, user_id: str) -> dict:
        """Get user details by user ID."""
        return self.user_repository.get_user_by_id(user_id)

    def list_users(self) -> list[dict]:
        """List all users in the database."""
        return self.user_repository.list_users()

    def delete_user(self, user_id: str) -> bool:
        """Delete a user by user ID."""
        return self.user_repository.delete_user(user_id)

    def update_user(self, user_id: str, user_data: dict) -> bool:
        """Update user details."""
        return self.user_repository.update_user(user_id, user_data)

    def get_user_by_username(self, username: str) -> dict:
        """Get user details by username."""
        return self.user_repository.get_user_by_username(username)
