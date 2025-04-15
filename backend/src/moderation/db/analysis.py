# models/content_analysis.py
import uuid
from datetime import datetime

from moderation.db.base import Base
from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID


class ContentAnalysis(Base):
    __tablename__ = "content_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"))
    flagged = Column(Boolean, default=False)
    score = Column(Float)
    model_version = Column(String)
    analysis_metadata = Column(JSON)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
