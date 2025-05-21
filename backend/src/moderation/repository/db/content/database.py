from typing import Callable, ContextManager, List

from moderation.db.analysis import ContentAnalysis as DBContentAnalysis
from moderation.db.content import Content as DBContent
from moderation.repository.db.content.base import AbstractDBContentRepository, Content
from sqlalchemy.orm import Session


def from_record(record: DBContent) -> Content:
    """Convert a database record to a Content object."""
    return Content(
        user_id=record.user_id,
        username=record.username,
        title=record.title,
        body=record.body,
        tags=record.tags,
        localization=record.localization,
        source=record.source,
        id=str(record.id),
        status=record.status,
        created_at=record.created_at.isoformat() if record.created_at else None,
        updated_at=record.updated_at.isoformat() if record.updated_at else None,
        image_paths=record.image_paths,
    )


class DatabaseContentRepository(AbstractDBContentRepository):
    """Database implementation of the content repository."""

    def __init__(self, db: Callable[[], ContextManager[Session]]) -> None:
        """Initialize the repository with a database session factory."""
        self.db = db

    def list(self, status: str | None = None) -> List[Content]:
        """List all content."""
        with self.db() as session:
            query = session.query(DBContent).select_from(DBContent).join(DBContentAnalysis)
            if status:
                query = query.filter(DBContent.status == status)
            return [from_record(record) for record in query.all()]

    def get_by_id(self, content_id: str) -> Content | None:
        """Get content by ID."""
        with self.db() as session:
            record = session.query(DBContent).filter(DBContent.id == content_id).first()
            return from_record(record) if record else None

    def create(self, content: Content) -> Content:
        """Create new content."""
        with self.db() as session:
            record = DBContent(
                user_id=content.user_id,
                username=content.username,
                title=content.title,
                body=content.body,
                tags=content.tags,
                localization=content.localization,
                source=content.source,
                image_paths=content.image_paths,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return from_record(record)

    def update(self, content_id: str, data: Content) -> Content | None:
        """Update content properties."""
        with self.db() as session:
            record = session.query(DBContent).filter(DBContent.id == content_id).first()
            if not record:
                return None
            for key, value in data.items():
                setattr(record, key, value)
            session.commit()
            session.refresh(record)
            return from_record(record)

    def update_status(self, content_id: str, status: str) -> Content | None:
        """Update content moderation status."""
        with self.db() as session:
            record = session.query(DBContent).filter(DBContent.id == content_id).first()
            if not record:
                return None
            record.status = status
            session.commit()
            session.refresh(record)
            return from_record(record)

    def delete(self, content_id: str) -> bool:
        """Delete content by ID."""
        with self.db() as session:
            record = session.query(DBContent).filter(DBContent.id == content_id).first()
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True
