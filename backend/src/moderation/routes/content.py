import logging
from http import HTTPStatus
from typing import Tuple

from dependency_injector.wiring import Provide, inject
from moderation.cache.redis import invalidate_cache
from moderation.constants.general import DASHBOARD_SUMMARY
from moderation.core.container import Container
from moderation.repository.db.content.base import Content
from moderation.service.content import ContentService
from moderation.service.kafka import KafkaProducerService
from moderation.service.storage import Storage
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)


@invalidate_cache(DASHBOARD_SUMMARY)
@inject
def create_content(
    body: dict,
    images: list[FileStorage] | None = None,
    documents: list[FileStorage] | None = None,
    storage_service: Storage = Provide[Container.storage_service],
    content_service: ContentService = Provide[Container.content_service],
    kafka: KafkaProducerService = Provide[Container.kafka_producer_service],
) -> Tuple[Content, HTTPStatus]:
    stored_images = storage_service.save(images if images else [])
    stored_documents = storage_service.save(documents if documents else [])
    content = content_service.create_content(body, stored_images.filenames, stored_documents.filenames)
    kafka.send_message_for_text_classifier(content.id, content.title + content.body, message_type="text")
    kafka.send_message_for_file_classifier_bulk(content.id, stored_images, message_type="image")
    kafka.send_message_for_file_classifier_bulk(content.id, stored_documents, message_type="document")
    return content, HTTPStatus.CREATED
