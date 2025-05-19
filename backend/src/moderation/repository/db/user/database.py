from moderation.db.user import User as DBUser
from moderation.repository.db.user.base import AbstractUserRepository, User, UserCreate, to_user
from sqlalchemy.orm import Session


class DatabaseUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_user(self, user: UserCreate) -> User:
        user = DBUser(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return to_user(user)

    def get_user_by_id(self, user_id: str) -> User | None:
        user = self.session.query(DBUser).filter(DBUser.id == user_id).first()
        return to_user(user) if user else None

    def get_user_by_username(self, username: str) -> User | None:
        user = self.session.query(DBUser).filter(DBUser.username == username).first()
        return to_user(user) if user else None

    def delete_user(self, user_id: str) -> bool:
        user = self.session.query(DBUser).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def list_users(self) -> list[User]:
        users = self.session.query(DBUser).all()
        return [to_user(user) for user in users]

    def update_user(self, user_id: str, user_data: dict) -> bool:
        user = self.session.query(DBUser).filter_by(id=user_id).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.session.commit()
            return True
        return False

    def get_by_criteria(self, **kwargs):
        return self.session.query(DBUser).filter_by(**kwargs).first()
