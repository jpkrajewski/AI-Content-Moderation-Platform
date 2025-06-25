import logging

from moderation.pipelines import get_pipeline, PipelineType
from moderation.repository.db.analysis.base import AnalysisResult
from moderation.workers.worker_context import get_worker_context, WorkerContext


logger = logging.getLogger(__name__)

async def run_moderation_pipeline(
        content_id: str,
        pipeline_type: str,
        filepath: str | None = None,
):
    async with get_worker_context() as context:
        worker = ModerationPipelineWorker(context=context)
        return await worker.run(content_id=content_id, pipeline_type=pipeline_type, filepath=filepath)



class ModerationPipelineWorker:
    def __init__(self, context: WorkerContext):
        self.context = context
        self.analysis_service = self.context.analysis_service
        self.content_service = self.context.content_service


    async def run(self, content_id: str, pipeline_type: str, filepath: str | None):
        logger.info(f"[run_moderation_pipeline] start for content_id: {content_id} pipeline_type: {pipeline_type}")

        type_ = PipelineType(pipeline_type)
        pipeline = get_pipeline(type_)
        input_ = self.get_input_data(content_id=content_id, pipeline_type=type_, filepath=filepath)
        results = await pipeline.process(input_)
        analysis_results = []
        for result in results:
            analysis = AnalysisResult(
                content_id=content_id,
                content_type=result.content_type,
                automated_flag=result.automated_flag,
                automated_flag_reason=result.automated_flag_reason,
                model_version=result.model_version,
                analysis_metadata=result.analysis_metadata,
                filename=filepath,
            )
            analysis_results.append(analysis)

        result = self.analysis_service.save_analysis_result_bulk(content_id, analysis_results)
        if result:
            logger.info(f"[run_moderation_pipeline] success for content_id: {content_id} pipeline_type: {pipeline_type}")
        else:
            logger.info(f"[run_moderation_pipeline] fail for content_id: {content_id} pipeline_type: {pipeline_type}")

    def get_input_data(self, content_id: str, pipeline_type: PipelineType, filepath: str | None):
        content = self.content_service.get_content(content_id=content_id)
        if content is None:
            logger.error(f"Content {content_id} not found.")

        if PipelineType.TEXT == pipeline_type:
            return content.body
        return filepath


