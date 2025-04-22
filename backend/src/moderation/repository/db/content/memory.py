from typing import Dict, List

from moderation.repository.db.content.base import AbstractDBContentRepository, Content


class InMemoryContentRepository(AbstractDBContentRepository):
    """In-memory implementation of the content repository for testing purposes."""

    def __init__(self) -> None:
        self.contents: Dict[str, Content] = {}
        self.counter = 0

    def list(self, status: str) -> List[Content]:
        """List all content."""
        return list(self.contents.values())

    def get_by_id(self, content_id: str) -> Content:
        """Get content by ID."""
        return self.contents.get(content_id)

    def create(self, content: Content) -> Content:
        """Create new content."""
        self.counter += 1
        content["id"] = str(self.counter)
        content["created_at"] = content["timestamp"]
        content["updated_at"] = content["timestamp"]
        content["status"] = "pending"
        content.pop("timestamp", None)
        self.contents[content["id"]] = content
        return Content(**content)

    def update(self, content_id: str, data: Content) -> Content:
        """Update content properties."""
        if content_id in self.contents:
            self.contents[content_id].update(data)
            return self.contents[content_id]
        return None

    def update_status(self, content_id: str, status: str) -> Content:
        """Update content moderation status."""
        if content_id in self.contents:
            self.contents[content_id].status = status
            return self.contents[content_id]
        return None

    def delete(self, content_id: str) -> bool:
        """Delete content by ID."""
        if content_id in self.contents:
            del self.contents[content_id]
            return True
        return False
