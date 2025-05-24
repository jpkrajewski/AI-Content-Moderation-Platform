from http import HTTPStatus
from typing import List, Literal
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.repository.db.content.base import Content
from moderation.service.content import ContentService, ContentWithAnalysis


@inject
def list_pending_content(
    content_service: ContentService = Provide[Container.content_service],
) -> tuple[List[ContentWithAnalysis], Literal[HTTPStatus.OK]]:
    """List all pending content"""
    return content_service.list_pending(), HTTPStatus.OK


@inject
def get_content_analysis(
    content_id: str, content_service: ContentService = Provide[Container.content_service]
) -> tuple[ContentWithAnalysis, Literal[HTTPStatus.OK]]:
    result = content_service.get_analysis_result(content_id)
    return result, HTTPStatus.OK


@inject
def approve_content(
    content_id: str, user: UUID, content_service: ContentService = Provide[Container.content_service]
) -> tuple[Content, Literal[HTTPStatus.OK]]:
    """Approve content by ID"""
    return content_service.update_content_status(content_id, user, "approved"), HTTPStatus.OK


@inject
def reject_content(
    content_id: str, user: UUID, content_service: ContentService = Provide[Container.content_service]
) -> tuple[Content, Literal[HTTPStatus.OK]]:
    """Reject content by ID"""
    return content_service.update_content_status(content_id, user, "rejected"), HTTPStatus.OK


@inject
def flag_content(
    content_id: str, user: UUID, content_service: ContentService = Provide[Container.content_service]
) -> tuple[Content, Literal[HTTPStatus.OK]]:
    """Flag content by ID"""
    return content_service.update_content_status(content_id, user, "flagged"), HTTPStatus.OK
