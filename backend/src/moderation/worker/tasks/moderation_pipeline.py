import logging

from moderation.worker.app import worker_app
from moderation.worker.tasks.helper import run_async
from moderation.workers import moderation_pipeline_worker

logger = logging.getLogger()


@worker_app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def run_moderation_pipeline(content_id: str, pipeline_type: str, filepath: str | None = None) -> None:
    logging.info(f"[run_moderation_pipeline] start")
    run_async(
        moderation_pipeline_worker.run_moderation_pipeline(
            content_id=content_id,
            pipeline_type=pipeline_type,
            filepath=filepath
        )
    )
    logging.info("[run_moderation_pipeline] done")
