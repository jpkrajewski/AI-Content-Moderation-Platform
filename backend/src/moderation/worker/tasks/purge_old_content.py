import logging

from moderation.worker.app import worker_app
from moderation.worker.tasks.helper import run_async
from moderation.workers import purge_old_content_worker

logger = logging.getLogger()


@worker_app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def purge_old_content() -> None:
    logging.info("[purge_old_content] start")
    run_async(purge_old_content_worker.run_purge_old_content())
    logging.info("[purge_old_content] done")
