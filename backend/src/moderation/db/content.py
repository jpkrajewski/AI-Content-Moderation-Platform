# models/content_service.py
import uuid
from datetime import datetime
from typing import List

from moderation.db.base import Base
from sqlalchemy import ARRAY, JSON, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Content(Base):
    __tablename__ = "content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    username = Column(String, nullable=True)  # Optional for denormalization/fallback
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tags: Column[List[str]] = Column(ARRAY(String), default=[])
    localization = Column(JSON, nullable=True)  # language, region
    source = Column(String, nullable=False)  # e.g. "acme_corp"
    status = Column(String(50), default="pending")  # pending, approved, rejected, flagged
    image_paths: Column[List[str]] = Column(ARRAY(String), default=[])  # List of image paths
    document_paths: Column[List[str]] = Column(ARRAY(String), default=[])  # List of document paths
    video_paths: Column[List[str]] = Column(ARRAY(String), default=[])
    audio_paths: Column[List[str]] = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    analysis = relationship(
        "ContentAnalysis",
        back_populates="content",
        cascade="all, delete-orphan",
        lazy="select",  # or "joined" if you want it eagerly loaded
    )
