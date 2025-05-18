# models/content.py
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class CustomerContentCreatorUser:
    __tablename__ = "customer_content_creator_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False)  # e.g. "acme_corp"
    user_id = Column(UUID(as_uuid=True), nullable=False)
    username = Column(String, nullable=True)
    reputation_score = Column(Integer, default=0)
    flagged_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
