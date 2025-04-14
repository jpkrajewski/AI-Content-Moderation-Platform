# models/moderation_action.py
import uuid
from datetime import datetime

from moderation.db.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID


class ModerationAction(Base):
    __tablename__ = "moderation_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"))
    moderator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(50), nullable=False)  # approve, reject, flag
    reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
