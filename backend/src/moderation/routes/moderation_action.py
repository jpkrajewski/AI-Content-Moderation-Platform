from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.service.content import ContentService


@inject
def list_pending_content(content_service: ContentService = Provide[Container.content_service]):
    """List all pending content"""
    return content_service.list_pending()


@inject
def get_content_analysis(content_id, content_service: ContentService = Provide[Container.content_service]):
    result, http = content_service.get_analysis_result(content_id)
    return result, http


@inject
def approve_content(content_id: str, content_service: ContentService = Provide[Container.content_service]):
    """Approve content by ID"""
    return content_service.update_content_status(content_id, "approved")


@inject
def reject_content(content_id: str, content_service: ContentService = Provide[Container.content_service]):
    """Reject content by ID"""
    return content_service.update_content_status(content_id, "rejected")


@inject
def flag_content(content_id: str, content_service: ContentService = Provide[Container.content_service]):
    """Flag content by ID"""
    return content_service.update_content_status(content_id, "flagged")
