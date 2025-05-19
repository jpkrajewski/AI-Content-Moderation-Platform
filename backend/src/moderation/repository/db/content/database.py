from typing import List

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

    def __init__(self, session: Session):
        self.session = session

    def list(self, status: str | None = None) -> List[Content]:
        """List all content."""
        if status:
            return (
                self.session.query(DBContent)
                .select_from(DBContent)
                .join(DBContentAnalysis)
                .filter(DBContent.status == status)
                .all()
            )
        return self.session.query(DBContent).select_from(DBContent).join(DBContentAnalysis).all()

    def get_by_id(self, content_id: str) -> Content:
        """Get content by ID."""
        return self.session.query(DBContent).filter(DBContent.id == content_id).first()

    def create(self, content: Content) -> Content:
        """Create new content."""
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
        self.session.add(record)
        self.session.commit()
        return from_record(record)

    def update(self, content_id: str, data: Content) -> Content:
        """Update content properties."""
        content = self.get_by_id(content_id)
        if content:
            for key, value in data.items():
                setattr(content, key, value)
            self.session.commit()
            return from_record(content)
        return None

    def update_status(self, content_id: str, status: str) -> Content:
        """Update content moderation status."""
        content = self.get_by_id(content_id)
        if content:
            content.status = status
            self.session.commit()
            return from_record(content)
        return None

    def delete(self, content_id: str) -> bool:
        """Delete content by ID."""
        content = self.get_by_id(content_id)
        if content:
            self.session.delete(content)
            self.session.commit()
            return True
        return False
