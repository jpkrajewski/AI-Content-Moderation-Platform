import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, ContextManager, List
from uuid import UUID

from moderation.db.analysis import ContentAnalysis as DBContentAnalysis
from moderation.db.content import Content as DBContent
from moderation.db.moderation import ModerationAction as DBModerationAction
from moderation.repository.db.content.base import AbstractDBContentRepository, Content, content_with_analysis
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, subqueryload

logger = logging.getLogger(__name__)


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
        document_paths=record.document_paths,
    )


@dataclass
class ContentSubmissionCounts:
    """Data class to hold submission counts."""

    today: int
    week: int
    month: int


class DatabaseContentRepository(AbstractDBContentRepository):
    """Database implementation of the content repository."""

    def __init__(self, db: Callable[[], ContextManager[Session]]) -> None:
        """Initialize the repository with a database session factory."""
        self.db = db

    def list(self, status: str | None = None, offset: int = 0, limit: int = 10) -> List[Content]:
        """
        List content with optional status filtering and pagination.

        Args:
            status (str | None): The status of the content to filter by (e.g., "pending").
            offset (int): The starting point for pagination (default is 0).
            limit (int): The number of items to fetch (default is 10).

        Returns:
            List[Content]: A list of content records.
        """
        with self.db() as session:
            query = session.query(DBContent).select_from(DBContent).outerjoin(DBContentAnalysis)

            # Apply status filter if provided
            if status:
                query = query.filter(DBContent.status == status)

            # Apply pagination
            query = query.offset(offset).limit(limit)

            # Fetch and return the results
            return [from_record(record) for record in query.all()]

    def list_with_analysis(self, status: str, offset: int, limit: int) -> List[Content]:
        with self.db() as session:
            content_list = (
                session.query(DBContent)
                .options(subqueryload(DBContent.analysis))
                .filter(DBContent.status == status)
                .order_by(DBContent.id)
                .order_by(DBContent.created_at)
                .offset(offset)
                .limit(limit)
                .all()
            )
            logger.info(f"Content analysis count: {len(content_list)}")
            return [content_with_analysis(content, content.analysis) for content in content_list]

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
                document_paths=content.document_paths,
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

    def update_status(self, content_id: str, user: UUID, status: str) -> Content | None:
        """Update content moderation status."""
        with self.db() as session:
            try:
                record = session.query(DBContent).filter(DBContent.id == content_id).one()

                # Try to get existing moderation action by this user on this content
                mod_action = (
                    session.query(DBModerationAction)
                    .filter(and_(DBModerationAction.content_id == content_id, DBModerationAction.moderator_id == user))
                    .one_or_none()
                )

                if mod_action:
                    mod_action.action = status
                    mod_action.created_at = datetime.now(timezone.utc)
                else:
                    mod_action = DBModerationAction(
                        content_id=content_id,
                        moderator_id=user,
                        action=status,
                        reason="",
                        created_at=datetime.now(timezone.utc),
                    )
                    session.add(mod_action)
                record.status = status
                return from_record(record)
            except NoResultFound:
                return None

    def delete(self, content_id: str) -> bool:
        """Delete content by ID."""
        with self.db() as session:
            record = session.query(DBContent).filter(DBContent.id == content_id).first()
            if not record:
                return False
            session.delete(record)
            session.commit()
            return True
