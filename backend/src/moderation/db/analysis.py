# models/content_analysis.py
import uuid
from datetime import datetime

from moderation.db.base import Base
from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ContentAnalysis(Base):
    __tablename__ = "content_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"))
    content_type = Column(String, nullable=False)
    automated_flag = Column(Boolean, default=False)
    automated_flag_reason = Column(String, nullable=True)
    model_version = Column(String)
    analysis_metadata = Column(JSON)
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    content = relationship("Content", back_populates="analysis")
