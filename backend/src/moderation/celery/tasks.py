import time

from .celery import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def analyze_content(self, content_id: str):
    try:
        print(f"Analyzing content: {content_id}")
        time.sleep(2)  # simulate processing
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task
def generate_summary_report():
    print("Generating moderation report...")
    # ...generate and store or email a report...
