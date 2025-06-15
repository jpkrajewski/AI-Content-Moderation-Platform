import logging

from moderation.worker.app import worker_app
from moderation.worker.tasks.helper import run_async
from moderation.workers import daily_email_worker

logger = logging.getLogger()


@worker_app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def run_send_daily_email() -> None:
    logger.info("[run_send_daily_email] start")
    run_async(daily_email_worker.run_send_daily_email())
    logger.info("[run_send_daily_email] done")
