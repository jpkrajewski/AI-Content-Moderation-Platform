import uuid
from datetime import datetime
from typing import List

from moderation.db.base import Base
from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class ClientAccess(Base):
    __tablename__ = "access"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False)  # e.g. "acme_corp"
    api_key = Column(String, nullable=False, unique=True)  # hashed api key
    current_scope: Column[List[str]] = Column(ARRAY(String), nullable=False)  # e.g. "moderation", "content"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)  # Number of times the API key has been used
    is_active = Column(Boolean, default=True)  # Whether the API key is active or not
