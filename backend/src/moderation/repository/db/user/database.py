from moderation.db.user import User
from moderation.repository.db.user.base import AbstractUserRepository
from sqlalchemy.orm import Session


class DatabaseUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_user(self, user_id: str, user_data: dict) -> bool:
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        return True

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.to_dict() if user else None

    def get_user_by_username(self, username: str) -> dict | None:
        user = self.session.query(User).filter_by(username=username).first()
        return user.to_dict() if user else None

    def delete_user(self, user_id: str) -> bool:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def list_users(self) -> list[dict]:
        users = self.session.query(User).all()
        return [user.to_dict() for user in users]

    def update_user(self, user_id: str, user_data: dict) -> bool:
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.session.commit()
            return True
        return False
