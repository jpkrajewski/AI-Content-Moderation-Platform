from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, ContextManager, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import func

from moderation.db.client_api_key import ClientApiKey as DBClientApiKey  # Assuming this is your DB model
from moderation.repository.db.client_api_key.base import AbstractClientApiKeyRepository, ClientApiKey
from sqlalchemy.orm import Session


def from_record(record: DBClientApiKey) -> ClientApiKey:
    """Convert a database record to a ClientApiKey object."""
    return ClientApiKey(
        id=str(record.id),
        source=record.source,
        client_id=record.client_id,
        api_key=record.api_key,
        current_scope=record.current_scope,
        created_at=record.created_at.isoformat() if record.created_at else None,
        updated_at=record.updated_at.isoformat() if record.updated_at else None,
        last_accessed=record.last_accessed.isoformat() if record.last_accessed else None,
        access_count=record.access_count,
        is_active=record.is_active,
    )


@dataclass
class ApiKeyUsageStats:
    """Data class to hold API key usage statistics."""

    total_keys: int
    active_keys: int
    inactive_keys: int


class DatabaseClientApiKeyRepository(AbstractClientApiKeyRepository):
    """Database implementation of the client API key repository."""

    def __init__(self, db: Callable[[], ContextManager[Session]]) -> None:
        """Initialize the repository with a database session context factory."""
        self.db = db

    def list(self, client_id: str | None = None, offset: int | None = None, limit: int | None = None) -> List[ClientApiKey]:
        """List all API keys, optionally filtered by client ID."""
        with self.db() as session:
            query = session.query(DBClientApiKey)
            if client_id:
                query = query.filter(DBClientApiKey.client_id == client_id)
            if offset:
                query = query.offset(offset - 1)
            if limit:
                query = query.limit(limit)
            return [from_record(record) for record in query.all()]

    def get_by_id(self, api_key_id: str) -> Optional[ClientApiKey]:
        """Get an API key by its ID."""
        with self.db() as session:
            record = session.query(DBClientApiKey).filter(DBClientApiKey.id == api_key_id).first()
            return from_record(record) if record else None

    def get_by_api_key(self, api_key_id: str) -> Optional[ClientApiKey]:
        """Get an API key by its API Key."""
        with self.db() as session:
            query = session.query(DBClientApiKey).filter(DBClientApiKey.api_key == api_key_id).first()
            return from_record(query) if query else None

    def create(self, api_key: ClientApiKey) -> ClientApiKey:
        """Create a new API key."""
        with self.db() as session:
            record = DBClientApiKey(
                id=UUID(api_key.id),
                source=api_key.source,
                client_id=api_key.client_id,
                api_key=api_key.api_key,
                current_scope=api_key.current_scope,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                is_active=True,
            )
            session.add(record)
            return from_record(record)

    def update(self, api_key_id: str, data: dict) -> Optional[ClientApiKey]:
        """Update an API key's properties."""
        with self.db() as session:
            record = session.query(DBClientApiKey).filter(DBClientApiKey.id == api_key_id).first()
            if not record:
                return None
            for key, value in data.items():
                setattr(record, key, value)
            record.updated_at = datetime.now(timezone.utc)
            return from_record(record)

    def deactivate(self, api_key_id: str) -> Optional[ClientApiKey]:
        """Deactivate an API key."""
        with self.db() as session:
            record = session.query(DBClientApiKey).filter(DBClientApiKey.id == api_key_id).first()
            if not record:
                return None
            record.is_active = False
            record.updated_at = datetime.now(timezone.utc)
            return from_record(record)

    def reactivate(self, api_key_id: str) -> Optional[ClientApiKey]:
        """Reactivate an API key."""
        with self.db() as session:
            record = session.query(DBClientApiKey).filter(DBClientApiKey.id == api_key_id).first()
            if not record:
                return None
            record.is_active = True
            record.updated_at = datetime.now(timezone.utc)
            return from_record(record)

    def delete(self, api_key_id: str) -> bool:
        """Delete an API key by its ID."""
        with self.db() as session:
            record = session.query(DBClientApiKey).filter(DBClientApiKey.id == api_key_id).first()
            if not record:
                return False
            session.delete(record)
            return True

    def get_usage_stats(self) -> ApiKeyUsageStats:
        """Get usage statistics for API keys."""
        with self.db() as session:
            total_keys = session.query(DBClientApiKey).count()
            active_keys = session.query(DBClientApiKey).filter(DBClientApiKey.is_active).count()
            inactive_keys = total_keys - active_keys
            return ApiKeyUsageStats(
                total_keys=total_keys,
                active_keys=active_keys,
                inactive_keys=inactive_keys,
            )

    def get_active_and_deactivated_count(self) -> Tuple[int, int]:
        with self.db() as session:
            count_label = func.count(DBClientApiKey.id).label("count")

            results = (
                session.query(DBClientApiKey.is_active.label("is_active"), count_label)
                .group_by(DBClientApiKey.is_active)
                .all()
            )

            count_by_status = {row.is_active: row.count for row in results}

            return count_by_status.get(True, 0), count_by_status.get(False, 0)
