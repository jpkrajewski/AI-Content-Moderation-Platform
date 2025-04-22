import logging
import sys
from typing import Callable

from kafka.consumer.fetcher import ConsumerRecord
from moderation.ai.image import image_moderation
from moderation.ai.models import ClassifyResult
from moderation.ai.text import text_moderation
from moderation.db.analysis import ContentAnalysis
from moderation.db.session import get_db
from moderation.kafka.models import KafkaModerationMessage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("log.log", mode="a"),
    ],
)
logger = logging.getLogger("moderation.consumer")


def save_result(
    content_id: str,
    result: ClassifyResult,
) -> bool:
    """Save the moderation result to the database."""
    record = ContentAnalysis(
        content_id=content_id,
        content_type=result.content_type,
        automated_flag=result.automated_flag,
        autmotated_flag_reason=result.autmotated_flag_reason,
        model_version=result.model_version,
        analysis_metadata=result.analysis_metadata,
    )

    try:
        with get_db() as session:
            session.add(record)
            session.commit()
            return True
    except Exception as e:
        logger.error(f"Failed to save moderation result: {e}")
        return False


def get_classifier(message: KafkaModerationMessage) -> Callable[[str], ClassifyResult] | None:
    match message.type:
        case "image":
            return image_moderation.classify
        case "text":
            return text_moderation.classify
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
