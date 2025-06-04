import logging
from http import HTTPStatus
from typing import List, Literal
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.repository.db.content.base import Content
from moderation.routes.display.models import UiInfo
from moderation.service import ClientApiKeyService
from moderation.service.content.content_service import ContentService, ContentWithAnalysis

logger = logging.getLogger(__name__)

@inject
def info(
    content_service: ContentService = Provide[Container.content_service],
    api_key_service: ClientApiKeyService = Provide[Container.api_key_service]
) -> tuple[UiInfo, HTTPStatus]:
    try:
        data =  UiInfo.from_info(
            contents=content_service.get_info(),
            api_keys=api_key_service.get_info(),
        ), HTTPStatus.OK
        return data

    except Exception as e:
        logger.error(f"Failed to get display info: {e}")
        return {"detail": "Failed to fetch info"}, HTTPStatus.INTERNAL_SERVER_ERROR