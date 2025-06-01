import logging

from rgmx.worker.app import worker_app
from rgmx.worker.tasks.async_task_helper import run_async
from rgmx.workers import optimization_post_processing_worker

logger = logging.getLogger()


@worker_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def run_moderation_pipeline(self, content_id: str):
    logging.info("[run_moderation_pipeline] start")

    run_async(
        optimization_post_processing_worker.handle_optimization_results(
            optimization_task_id=simulation_id,
        )
    )
    logging.info("[run_moderation_pipeline] done")
