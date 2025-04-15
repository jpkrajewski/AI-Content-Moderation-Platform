from http import HTTPStatus
from typing import Dict, Tuple

from moderation.kafka.producer import publish_content_message


def create_content(body: dict) -> Tuple[Dict, HTTPStatus]:
    """Create new content"""
    content_id = "content_123"  # In a real implementation, this would be generated
    publish_content_message(body.get("title"))
    return {
        "id": content_id,
        "title": body["title"],
        "body": body["body"],
        "tags": body.get("tags", []),
        "status": "pending",
        "created_at": "2025-04-13T12:00:00Z",
    }, HTTPStatus.CREATED


def list_content(status: str | None = None):
    """List all content with optional status filter"""
    content_list = [
        {
            "id": "content_123",
            "title": "First content item",
            "tags": ["tag1", "tag2"],
            "status": "pending",
            "created_at": "2025-04-12T10:00:00Z",
        },
        {
            "id": "content_456",
            "title": "Second content item",
            "tags": ["tag2", "tag3"],
            "status": "approved",
            "created_at": "2025-04-13T09:30:00Z",
        },
    ]

    if status:
        content_list = [item for item in content_list if item["status"] == status]

    return content_list, HTTPStatus.OK


def get_content(content_id: str):
    """Get specific content by ID"""
    return {
        "id": content_id,
        "title": "Sample content",
        "body": "This is the full content body text.",
        "tags": ["sample", "content"],
        "status": "pending",
        "created_at": "2025-04-13T08:15:00Z",
        "updated_at": "2025-04-13T08:15:00Z",
    }, HTTPStatus.OK
