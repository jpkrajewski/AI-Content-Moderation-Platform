import asyncio
import logging

from dependency_injector.wiring import Provide, inject
from kafka.consumer.fetcher import ConsumerRecord
from moderation.core.container import Container
from moderation.kafka.models import KafkaModerationMessage
from moderation.pipelines import PipelineType, get_pipeline
from moderation.repository.db.analysis.base import AnalysisResult
from moderation.service.analysis import AnalysisService

logger = logging.getLogger("moderation")


def process_message(record: ConsumerRecord) -> None:
    try:
        message = KafkaModerationMessage(**record.value)
        asyncio.run(process_pipeline_async(message))
    except Exception as e:
        logger.exception(f"Failed to process message: {e}")
        logger.error(f"Consumer record: {record}")
        return


@inject
async def process_pipeline_async(
    message: KafkaModerationMessage, service: AnalysisService = Provide[Container.analysis_service]
):
    pipeline = get_pipeline(PipelineType(message.type))
    results = await pipeline.process(message.get_input_data())
    logger.info(f"results: {results}")
    analysis_results = []
    for result in results:
        analysis = AnalysisResult(
            content_id=message.content_id,
            content_type=result.content_type,
            automated_flag=result.automated_flag,
            automated_flag_reason=result.automated_flag_reason,
            model_version=result.model_version,
            analysis_metadata=result.analysis_metadata,
            filename=message.filename,
        )
        analysis_results.append(analysis)

    logger.info(f"Saving analysis result: {analysis_results}")
    try:
        service.save_analysis_result_bulk(message.content_id, analysis_results)
    except Exception as e:
        logger.exception(f"Failed to save analysis result: {e}")
