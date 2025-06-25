import asyncio
import logging

from dependency_injector.wiring import Provide, inject
from kafka.consumer.fetcher import ConsumerRecord
from moderation.core.container import Container
from moderation.kafka.models import KafkaModerationMessage
from moderation.pipelines import PipelineType, get_pipeline
from moderation.repository.db.analysis.base import AnalysisResult
from moderation.service.analysis import AnalysisService
from moderation.worker.tasks.moderation_pipeline import run_moderation_pipeline

logger = logging.getLogger("moderation")


def process_message(record: ConsumerRecord) -> None:
    try:
        message = KafkaModerationMessage(**record.value)
        run_moderation_pipeline.delay(content_id=message.content_id,
            pipeline_type=message.type,
            filepath=message.filepath)
    except Exception as e:
        logger.exception(f"Failed to process message: {e}")
        logger.error(f"Consumer record: {record}")