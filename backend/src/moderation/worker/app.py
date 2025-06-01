from logging import StreamHandler

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger, worker_shutdown

from moderation.core.settings import settings
from moderation.worker.worker_json_log_formatter import WorkerJsonLogFormatter


def provide_worker_app() -> Celery:
    app = Celery(
        settings.CELERY_WORKER_APP_NAME,
        broker=settings.CELERY_WORKER_BROKER,
        backend=settings.CELERY_WORKER_BACKEND,
    )

    app.conf.timezone = "UTC"



worker_app = provide_worker_app()


@after_setup_logger.connect
@after_setup_task_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.handlers = []
    logger.propagate = False

    formatter = WorkerJsonLogFormatter()
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger

if __name__ == "__main__":
    worker_app.Worker().start()
