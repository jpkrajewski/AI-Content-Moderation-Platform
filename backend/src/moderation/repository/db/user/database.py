from typing import Callable, ContextManager

from moderation.db.user import User as DBUser
from moderation.repository.db.user.base import AbstractUserRepository, User, UserCreate, to_user
from sqlalchemy.orm import Session


class DatabaseUserRepository(AbstractUserRepository):
    def __init__(self, db: Callable[[], ContextManager[Session]]) -> None:
        """Initialize the repository with a database session."""
        self.db = db

    def save_user(self, user: UserCreate) -> User:
        with self.db() as session:
            db_user = DBUser(
                username=user.username,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role,
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return to_user(db_user)

    def get_user_by_id(self, user_id: str) -> User | None:
        with self.db() as session:
            user = session.query(DBUser).filter(DBUser.id == user_id).first()
            return to_user(user) if user else None

    def get_user_by_username(self, username: str) -> User | None:
        with self.db() as session:
            user = session.query(DBUser).filter(DBUser.username == username).first()
            return to_user(user) if user else None

    def delete_user(self, user_id: str) -> bool:
        with self.db() as session:
            user = session.query(DBUser).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False

    def list_users(self) -> list[User]:
        with self.db() as session:
            users = session.query(DBUser).all()
            return [to_user(user) for user in users]

    def update_user(self, user_id: str, user_data: dict) -> bool:
        with self.db() as session:
            user = session.query(DBUser).filter_by(id=user_id).first()
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                session.commit()
                return True
            return False

    def get_by_criteria(self, **kwargs) -> User | None:
        with self.db() as session:
            user = session.query(DBUser).filter_by(**kwargs).first()
            if user:
                return to_user(user)
            return None

    def get_password_hash_by_email(self, email) -> str | None:
        with self.db() as session:
            user = session.query(DBUser).filter_by(email=email).first()
            if user:
                return user.password_hash
            return None
