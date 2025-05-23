import logging
from typing import Callable, Optional

from dependency_injector.wiring import Provide, inject
from kafka.consumer.fetcher import ConsumerRecord
from moderation.ai.image import get_image_moderation
from moderation.ai.models import ClassifyResult
from moderation.ai.pii import get_pii_analyzer
from moderation.ai.text import get_text_classifier
from moderation.core.container import Container
from moderation.kafka.models import KafkaModerationMessage
from moderation.repository.db.analysis.base import AnalysisResult
from moderation.service.content import ContentService

logger = logging.getLogger("moderation")


def get_classifier(message_type: str) -> Callable[[str], ClassifyResult]:
    classifier = {
        "image": get_image_moderation().classify,
        "text": get_text_classifier().classify,
        "document": get_text_classifier().classify_from_document,
    }
    return classifier[message_type]


@inject
def save_analysis_result(
    content_id: str,
    result: ClassifyResult,
    filename: Optional[str] = None,
    content_service: ContentService = Provide[Container.content_service],
) -> bool:
    analysis = AnalysisResult(
        content_id=content_id,
        content_type=result.content_type,
        automated_flag=result.automated_flag,
        automated_flag_reason=result.automated_flag_reason,
        model_version=result.model_version,
        analysis_metadata=result.analysis_metadata,
        filename=filename,
    )

    logger.info(f"Saving analysis result: {analysis}")

    try:
        saved = content_service.save_analysis_result(content_id, analysis)
        logger.info(f"Saved analysis result: {saved}")
        return True
    except Exception as e:
        logger.exception(f"Failed to save analysis result: {e}")
        return False


def classify_and_save(message: KafkaModerationMessage) -> None:
    classification = get_classifier(message.type)(message.get_input_data())
    success = save_analysis_result(
        content_id=message.content_id,
        result=classification,
        filename=message.filename,
    )
    if success:
        logger.info(f"Processed and saved: {message.content_id} ({message.type})")
    else:
        logger.error(f"Failed to save result for: {message.content_id} ({message.type})")


@inject
def analyze_pii(
    message: KafkaModerationMessage,
    content_service: ContentService = Provide[Container.content_service],
):
    result = get_pii_analyzer().analyze(message.get_input_data())
    analysis = AnalysisResult(
        content_id=message.content_id,
        content_type=result.content_type,
        automated_flag=False,
        automated_flag_reason="",
        model_version=result.model_version,
        analysis_metadata=result.get_analysis_metadata(),
        filename=None,
    )
    logger.info(f"Saving PII analysis result: {analysis}")

    try:
        saved = content_service.save_analysis_result(message.content_id, analysis)
        logger.info(f"Saved PII analysis result: {saved}")
        return True
    except Exception as e:
        logger.exception(f"Failed to save PII analysis result: {e}")
        return False


def process_message(record: ConsumerRecord) -> None:
    message = KafkaModerationMessage(**record.value)
    message.validate()
    classify_and_save(message)
    if message.is_text():
        analyze_pii(message)
