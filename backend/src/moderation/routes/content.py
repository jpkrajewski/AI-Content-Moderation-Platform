import logging
from http import HTTPStatus
from typing import Tuple

from dependency_injector.wiring import Provide, inject
from moderation.cache.redis import invalidate_cache
from moderation.constants.general import DASHBOARD_SUMMARY
from moderation.core.container import Container
from moderation.pipelines.moderation.enums import PipelineType
from moderation.repository.db.content.base import Content
from moderation.service.content.content_service import ContentService
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
    videos: list[FileStorage] | None = None,
    audios: list[FileStorage] | None = None,
    storage_service: Storage = Provide[Container.storage_service],
    content_service: ContentService = Provide[Container.content_service],
    kafka: KafkaProducerService = Provide[Container.kafka_producer_service],
) -> Tuple[Content, HTTPStatus]:
    stored_images = storage_service.save(images if images else [])
    stored_documents = storage_service.save(documents if documents else [])
    stored_videos = storage_service.save(videos if videos else [])
    stored_audios = storage_service.save(audios if audios else [])
    content = content_service.create_content(
        body, stored_images.filenames, stored_documents.filenames, stored_videos.filenames, stored_audios.filenames
    )
    kafka.send_message_for_text_classifier(content.id, content.title + content.body, message_type=PipelineType.TEXT)
    kafka.send_message_for_file_classifier_bulk(content.id, stored_images, message_type=PipelineType.IMAGE)
    kafka.send_message_for_file_classifier_bulk(content.id, stored_documents, message_type=PipelineType.DOCUMENT)
    kafka.send_message_for_file_classifier_bulk(content.id, stored_videos, message_type=PipelineType.VIDEO)
    kafka.send_message_for_file_classifier_bulk(content.id, stored_audios, message_type=PipelineType.AUDIO)
    return content, HTTPStatus.CREATED
