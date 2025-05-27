from celery import Celery
from celery.schedules import crontab
from moderation.core.settings import settings

celery_app = Celery(
    "moderation",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,
)

celery_app.autodiscover_tasks(["moderation"])

beat_schedule = {
    "generate-daily-report": {
        "task": "moderation.tasks.generate_summary_report",
        "schedule": crontab(hour=0, minute=0),  # every day at midnight
    },
}
