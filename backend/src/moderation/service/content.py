from http import HTTPStatus
from typing import Any, Dict, List, Optional

from sqlalchemy import Tuple


class ContentService:
    """Service layer that coordinates between API endpoints and database."""

    def __init__(self, repository):
        self.repository = repository

    def create_content(self, body: Dict[str, Any]) -> Tuple[Dict[str, Any], HTTPStatus]:
        """Create new content and queue it for moderation."""
        content = self.repository.create(body)
        return content, HTTPStatus.CREATED

    def list_content(self, status: Optional[str] = None) -> Tuple[List[Dict[str, Any]], HTTPStatus]:
        """List all content with optional status filter."""
        content_list = self.repository.list(status)
        return content_list, HTTPStatus.OK

    def get_content(self, content_id: str) -> Tuple[Dict[str, Any], HTTPStatus]:
        """Get specific content by ID."""
        content = self.repository.get_by_id(content_id)
        if content:
            return content, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def update_content(self, content_id: str, data: Dict[str, Any]) -> Tuple[Dict[str, Any], HTTPStatus]:
        """Update content properties."""
        content = self.repository.update(content_id, data)
        if content:
            return content, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def update_content_status(self, content_id: str, status: str) -> Tuple[Dict[str, Any], HTTPStatus]:
        """Update content moderation status."""
        content = self.repository.update_status(content_id, status)
        if content:
            return content, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def delete_content(self, content_id: str) -> Tuple[Dict[str, Any], HTTPStatus]:
        """Delete content by ID."""
        success = self.repository.delete(content_id)
        if success:
            return {"message": f"Content {content_id} successfully deleted"}, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND
