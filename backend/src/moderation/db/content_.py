# models/content.py
import uuid
from datetime import datetime

from moderation.db.base import Base
from sqlalchemy import ARRAY, JSON, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID


class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    username = Column(String, nullable=True)  # Optional for denormalization/fallback
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(ARRAY(String), default=[])
    localization = Column(JSON, nullable=True)  # language, region
    source = Column(String, nullable=False)  # e.g. "acme_corp"
    status = Column(String(50), default="pending")  # pending, approved, rejected, flagged
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
