import logging
from typing import Callable

from dependency_injector.wiring import Provide, inject
from kafka.consumer.fetcher import ConsumerRecord
from moderation.ai.image import get_image_moderation
from moderation.ai.models import ClassifyResult
from moderation.ai.text import get_text_moderation
from moderation.core.container import Container
from moderation.kafka.models import KafkaModerationMessage
from moderation.repository.db.analysis.base import AnalysisResult
from moderation.service.content import ContentService

logger = logging.getLogger("moderation")


@inject
def save_result(
    content_id: str,
    result: ClassifyResult,
    content_service: ContentService = Provide[Container.content_service],
) -> bool:
    try:
        input_ = AnalysisResult(
            content_id=content_id,
            content_type=result.content_type,
            automated_flag=result.automated_flag,
            automated_flag_reason=result.automated_flag_reason,
            model_version=result.model_version,
            analysis_metadata=result.analysis_metadata,
        )
        result = content_service.save_analysis_result(content_id, input_)
        logger.info(f"Saved analysis result: {result}")
    except Exception as e:
        logger.error(f"Failed to save analysis result: {e}")
        return False
    return True


def get_classifier(message: KafkaModerationMessage) -> Callable[[str], ClassifyResult] | None:
    match message.type:
        case "image":
            return get_image_moderation().classify
        case "text":
            return get_text_moderation().classify
        case _:
            return None


def process_message(message: ConsumerRecord) -> None:
    try:
        result = KafkaModerationMessage(**message.value)
    except TypeError as e:
        logger.error(f"Failed to parse message: {e}")
        return
    classifier = get_classifier(result)
    if classifier is None:
        logger.error(f"Unsupported message type: {result.type}")
        return
    classification_result = classifier(result.message)
    logger.info(f"Classification result: {classification_result}")
    save_result(result.content_id, classification_result)
