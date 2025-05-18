from http import HTTPStatus
from typing import Dict, Tuple

from dependency_injector.wiring import Provide, inject
from flask import request
from moderation.core.container import Container
from moderation.service.content import ContentService
from moderation.service.image_storage import LocalImageStorage
from moderation.service.kafka import KafkaProducerService


@inject
def create_content(
    body: dict,
    content_service: ContentService = Provide[Container.content_service],
    kafka: KafkaProducerService = Provide[Container.kafka_producer_service],
) -> Tuple[Dict, HTTPStatus]:
    paths = LocalImageStorage().save_images(request.files.getlist("images"))
    content = content_service.create_content(body, paths)
    kafka.send_message_for_text_classifier(content.id, content.body, message_type="text")
    kafka.send_message_for_image_classifier_bulk(content.id, paths, message_type="image")
    return content, HTTPStatus.CREATED


@inject
def list_content(
    status: str | None = None, content_service: ContentService = Provide[Container.content_service]
) -> Tuple[Dict, HTTPStatus]:
    """List all content with optional status filter"""
    return content_service.list_content(status=status)


@inject
def get_content(
    content_id: str, content_service: ContentService = Provide[Container.content_service]
) -> Tuple[Dict, HTTPStatus]:
    """Get specific content by ID"""
    return content_service.get_content(content_id)
