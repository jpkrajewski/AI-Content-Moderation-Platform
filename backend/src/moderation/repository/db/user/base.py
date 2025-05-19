from abc import ABC, abstractmethod
from dataclasses import dataclass

from moderation.db.user import User as DBUser


@dataclass
class UserCreate:
    username: str
    email: str
    password_hash: str
    role: str = "moderator"


@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    role: str
    created_at: str
    updated_at: str


def to_user(user: DBUser) -> User:
    return User(
        id=str(user.id),
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        role=user.role,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
    )


class AbstractUserRepository(ABC):
    @abstractmethod
    def save_user(self, user: UserCreate) -> User:
        """Save the user data to the database."""

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None:
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
    def get_user_by_username(self, username: str) -> User | None:
        """Retrieve the user data by username from the database."""

    @abstractmethod
    def get_by_criteria(self, **kwargs) -> User | None:
        """Retrieve the user data by criteria from the database."""
