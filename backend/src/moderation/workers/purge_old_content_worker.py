import logging
from datetime import datetime, timedelta, timezone

from moderation.core.settings import settings
from moderation.db.content import Content
from moderation.repository.db.analysis.base import AnalysisResult
from moderation.workers.worker_context import WorkerContext, get_worker_context

logger = logging.getLogger(__name__)


async def run_purge_old_content():
    async with get_worker_context() as context:
        worker = PurgeOldContentWorker(context=context)
        return await worker.run()


class PurgeOldContentWorker:
    def __init__(self, context: WorkerContext):
        self.context = context
        self.analysis_repository = self.context.analysis_repository
        self.content_repository = self.context.content_repository

    async def run(self) -> None:
        logger.info("[PurgeOldContentWorker.run] Started]")
        cutoff_date = datetime.now(tz=timezone.utc) - timedelta(
            days=settings.CELERY_WORKER_PURGE_OLD_CONTENT_CUTOFF_DAYS
        )
        filters = [
            Content.updated_at < cutoff_date,
            Content.status == "pending",
        ]

        old_flagged_content = self.content_repository.list_by_criterion(*filters)
        old_flagged_content_ids = [content.id for content in old_flagged_content]

        filters = [
            AnalysisResult.content_id in old_flagged_content_ids,
        ]

        old_flagged_content_analysis = self.analysis_repository.list_by_criterion(*filters)
        old_flagged_content_analysis_ids = [analysis.id for analysis in old_flagged_content_analysis]

        self.analysis_repository.delete_bulk(old_flagged_content_analysis_ids)
        self.content_repository.delete_bulk(old_flagged_content_ids)

        logger.info("[PurgeOldContentWorker.run] Finished]")
