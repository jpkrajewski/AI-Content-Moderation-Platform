# models/content.py
import uuid
from datetime import datetime

from moderation.db.base import Base
from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID


class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(ARRAY(String))
    status = Column(String(50), default="pending")  # pending, approved, rejected, flagged
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
