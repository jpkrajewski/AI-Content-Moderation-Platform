from datetime import datetime, timezone

from moderation.db.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID


class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    path = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
