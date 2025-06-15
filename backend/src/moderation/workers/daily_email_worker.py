import logging
from datetime import date, datetime, timezone

from moderation.db.analysis import ContentAnalysis
from moderation.db.content import Content
from moderation.mailer import TemplateType, get_template, send_email
from moderation.workers.worker_context import WorkerContext, get_worker_context

logger = logging.getLogger(__name__)


async def run_send_daily_email():
    async with get_worker_context() as context:
        worker = DailyEmailWorker(context=context)
        return await worker.run()


class DailyEmailWorker:
    def __init__(self, context: WorkerContext):
        self.context = context
        self.content_repository = self.context.content_repository
        self.analysis_repository = self.context.analysis_repository

    async def run(self):
        logger.info("[DailyEmailWorker.run] Starting daily email worker]")
        today = date.today()
        start_of_day = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
        end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=timezone.utc)

        content_filter = [
            Content.created_at >= start_of_day,
            Content.created_at <= end_of_day,
        ]
        today_content = self.content_repository.list_by_criterion(*content_filter)

        analysis_filter = [
            ContentAnalysis.analyzed_at >= start_of_day,
            ContentAnalysis.analyzed_at <= end_of_day,
        ]
        today_analysis = self.analysis_repository.list_by_criterion(*analysis_filter)

        submitted_count = len(today_content)
        flagged_by_ai_count = sum(1 for a in today_analysis if a.automated_flag)
        moderator_reviewed_count = sum(1 for c in today_content if c.status in ["approved", "rejected"])
        rejected_count = sum(1 for c in today_content if c.status == "rejected")
        approved_count = sum(1 for c in today_content if c.status == "approved")

        template = get_template(TemplateType.DAILY)
        html = template.render(
            report_date=today.strftime("%B %d, %Y"),
            submitted_count=submitted_count,
            flagged_by_ai_count=flagged_by_ai_count,
            moderator_reviewed_count=moderator_reviewed_count,
            rejected_count=rejected_count,
            approved_count=approved_count,
            dashboard_url="https://yourplatform.com/moderation",
        )

        status = send_email(
            subject="Daily Email",
            html_content=html,
        )

        logger.info(f"[DailyEmailWorker.run] Daily Email Submitted: {status}]")
