from abc import ABC, abstractmethod


class AbstractUserRepository(ABC):
    @abstractmethod
    def save_user(self, user_id: str, user_data: dict) -> bool:
        """Save the user data to the database."""

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> dict | None:
        """Retrieve the user data from the database."""

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Delete the user data from the database."""

    @abstractmethod
    def list_users(self) -> list[dict]:
        """List all users in the database."""

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict) -> bool:
        """Update the user data in the database."""

    @abstractmethod
    def get_user_by_username(self, username: str) -> dict | None:
        """Retrieve the user data by username from the database."""
