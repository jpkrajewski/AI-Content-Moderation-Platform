import logging
from http import HTTPStatus
from typing import Dict, Tuple

from dependency_injector.wiring import Provide, inject
from moderation.cache.redis import invalidate_cache
from moderation.constants.cache import DASHBOARD_SUMMARY
from moderation.core.container import Container
from moderation.service.content import ContentService
from moderation.service.file_storage import Storage
from moderation.service.kafka import KafkaProducerService
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


@invalidate_cache(DASHBOARD_SUMMARY)
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
