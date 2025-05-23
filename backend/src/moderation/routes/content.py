import logging
from http import HTTPStatus
from typing import Dict, Tuple

from dependency_injector.wiring import Provide, inject
from moderation.core.container import Container
from moderation.service.content import ContentService
from moderation.service.file_storage import Storage
from moderation.service.kafka import KafkaProducerService
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


@inject
def create_content(
    body: dict,
    images: list[FileStorage] | None = None,
    documents: list[FileStorage] | None = None,
    content_service: ContentService = Provide[Container.content_service],
    kafka: KafkaProducerService = Provide[Container.kafka_producer_service],
) -> Tuple[Dict, HTTPStatus]:
    storage = Storage()
    stored_images = storage.save(images if images else [])
    stored_documents = storage.save(documents if documents else [])
    content = content_service.create_content(body, stored_images.filenames, stored_documents.filenames)
    kafka.send_message_for_text_classifier(content.id, content.title + content.body, message_type="text")
    kafka.send_message_for_image_classifier_bulk(content.id, stored_images, message_type="image")
    kafka.send_message_for_image_classifier_bulk(content.id, stored_documents, message_type="document")
    return content, HTTPStatus.CREATED


@inject
def list_content(
    status: str | None = None,
    content_service: ContentService = Provide[Container.content_service],
) -> Tuple[Dict, HTTPStatus]:
    """List all content with optional status filter."""
    try:
        return content_service.list_content(status=status), HTTPStatus.OK
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@inject
def get_content(
    content_id: str,
    content_service: ContentService = Provide[Container.content_service],
) -> Tuple[Dict, HTTPStatus]:
    """Get specific content by ID."""
    try:
        return content_service.get_content(content_id), HTTPStatus.OK
    except ValueError as e:
        return {"error": str(e)}, HTTPStatus.NOT_FOUND
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
