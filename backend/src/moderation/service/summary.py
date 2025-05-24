from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable, ContextManager, Dict

from moderation.db.analysis import ContentAnalysis as DBContentAnalysis
from moderation.db.content import Content as DBContent
from moderation.db.moderation import ModerationAction as DBModerationAction
from sqlalchemy import Float, and_, case, cast, func, text, true
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session


@dataclass
class ContentInsight:
    most_common_toxicity_labels: Dict[str, int]
    most_common_pii_types: Dict[str, int]
    pii_detected_rate: float


@dataclass
class StatusCounts:
    flagged: int
    rejected: int
    approved: int


@dataclass
class ModerationSummary:
    statuses: StatusCounts
    auto_flag_accuracy: float
    false_positive_rate: float


@dataclass
class SubmissionCounts:
    today: int
    week: int
    month: int


@dataclass
class ContentSummary:
    submission_counts: SubmissionCounts
    growth_rate: float
    peak_hours: Dict[int, int]
    submission_sources: Dict[str, int]


@dataclass
class DashboardSummary:
    content: ContentSummary
    moderation: ModerationSummary
    insights: ContentInsight


class SummaryService:
    def __init__(self, db: Callable[[], ContextManager[Session]]) -> None:
        self.db = db

    def summision_counts(self) -> SubmissionCounts:
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = now - timedelta(days=7)
        month_start = now.replace(day=1)
        with self.db() as session:
            counts = session.query(
                func.count(case((DBContent.created_at >= today_start, 1))).label("today"),
                func.count(case((DBContent.created_at >= week_start, 1))).label("week"),
                func.count(case((DBContent.created_at >= month_start, 1))).label("month"),
            ).one()
            today, week, month = counts
            return SubmissionCounts(
                today=today,
                week=week,
                month=month,
            )

    def growth_rate(self) -> float:
        """Calculate the growth rate of content submissions over the last week."""
        now = datetime.now(timezone.utc)
        week_start = now - timedelta(days=7)
        last_week_start = now - timedelta(days=14)
        with self.db() as session:
            growth = session.query(
                func.count(case((and_(DBContent.created_at >= week_start, DBContent.created_at < now), 1))).label(
                    "this_week"
                ),
                func.count(
                    case((and_(DBContent.created_at >= last_week_start, DBContent.created_at < week_start), 1))
                ).label("last_week"),
            ).one()
            this_week, last_week = growth
            if last_week == 0:
                return 0.0
            return (this_week - last_week) / last_week * 100.0 if last_week > 0 else 0.0

    def peak_submission_hours(self, top: int = 5) -> dict[int, int]:
        """Get the peak submission time."""
        with self.db() as session:
            peak_hours = (
                session.query(func.extract("hour", DBContent.created_at).label("hour"), func.count().label("count_"))
                .group_by("hour")
                .order_by(func.count().desc())
                .limit(top)
                .all()
            )
            if not peak_hours:
                return {}
            peak_dict = {int(row.hour): row.count_ for row in peak_hours}
            return peak_dict

    def sources(self, top: int | None = 5) -> dict[str, int]:
        """Get the top sources of content."""
        with self.db() as session:
            query = (
                session.query(DBContent.source, func.count(DBContent.id))
                .group_by(DBContent.source)
                .order_by(func.count(DBContent.id).desc())
            )
            if top:
                query = query.limit(top)
            return dict(query.all())

    def get_content_volume_and_flow(self) -> ContentSummary:
        """Get the dashboard summary including submission counts, growth rate, peak hours, and sources."""
        submission_counts = self.summision_counts()
        growth_rate = self.growth_rate()
        peak_hours = self.peak_submission_hours()
        submission_sources = self.sources()

        return ContentSummary(
            submission_counts=submission_counts,
            growth_rate=growth_rate,
            peak_hours=peak_hours,
            submission_sources=submission_sources,
        )

    def flagged_rejected_approved_counts(self) -> StatusCounts:
        """Get counts of flagged, rejected, and approved content."""
        with self.db() as session:
            counts = session.query(
                func.count(case((DBContent.status == "flagged", 1))).label("flagged"),
                func.count(case((DBContent.status == "rejected", 1))).label("rejected"),
                func.count(case((DBContent.status == "approved", 1))).label("approved"),
            ).one()
            flagged, rejected, approved = counts
            return StatusCounts(flagged=flagged, rejected=rejected, approved=approved)

    def auto_flag_accuracy(self) -> float:
        """Calculate the accuracy of automated flagging."""
        with self.db() as session:
            total_auto_flagged = (
                session.query(DBContent)
                .join(DBContentAnalysis, DBContent.id == DBContentAnalysis.content_id)
                .filter(DBContentAnalysis.automated_flag.is_(True))
                .count()
            )

            # Number of auto-flagged content later confirmed toxic (i.e., rejected)
            true_positives = (
                session.query(DBContent)
                .join(DBContentAnalysis, DBContent.id == DBContentAnalysis.content_id)
                .join(DBModerationAction, DBModerationAction.content_id == DBContent.id)
                .filter(DBContentAnalysis.automated_flag.is_(True), DBModerationAction.action != "rejected")
                .count()
            )

            if total_auto_flagged == 0:
                return 0.0

            return true_positives / total_auto_flagged

    def false_positive_rate(self) -> float:
        with self.db() as session:
            total_auto_flagged = (
                session.query(DBContent)
                .join(DBContentAnalysis, DBContent.id == DBContentAnalysis.content_id)
                .filter(DBContentAnalysis.automated_flag.is_(True))
                .count()
            )

            false_positives = (
                session.query(DBContent)
                .join(DBContentAnalysis, DBContent.id == DBContentAnalysis.content_id)
                .join(DBModerationAction, DBModerationAction.content_id == DBContent.id)
                .filter(DBContentAnalysis.automated_flag.is_(True), DBModerationAction.action == "approved")
                .count()
            )

            if total_auto_flagged == 0:
                return 0.0

            return false_positives / total_auto_flagged

    def moderation_outcomes(self) -> ModerationSummary:
        return ModerationSummary(
            statuses=self.flagged_rejected_approved_counts(),
            auto_flag_accuracy=self.auto_flag_accuracy(),
            false_positive_rate=self.false_positive_rate(),
        )

    def most_common_toxicity_label(self, top: int = 5) -> Dict[str, int]:
        with self.db() as session:
            # Use json_each_text for JSON column, casting if needed
            json_each = func.json_each_text(cast(DBContentAnalysis.analysis_metadata, postgresql.JSON)).table_valued(
                "key", "value"
            )

            subq = (
                session.query(
                    json_each.c.key.label("reason"),
                    cast(json_each.c.value, Float).label("score"),
                    DBContentAnalysis.id.label("content_id"),
                )
                .select_from(DBContentAnalysis)
                .join(json_each, true())
                .filter(
                    DBContentAnalysis.automated_flag.is_(True),
                    DBContentAnalysis.content_type == "text",
                )
                .subquery()
            )

            query = (
                session.query(subq.c.reason, func.count(subq.c.content_id).label("count"))
                .filter(subq.c.score > 0.7)
                .group_by(subq.c.reason)
                .order_by(func.count(subq.c.content_id).desc())
            )

            if top:
                query = query.limit(top)

            return {row.reason: row.count for row in query.all()}

    def most_common_pii_types(self, top: int = 5, score_threshold: float = 0.7) -> dict[str, int]:
        with self.db() as session:
            # Lateral join with json_array_elements on 'results'
            # Since SQLAlchemy lacks direct lateral join support with json_array_elements, use text()
            sql = text(
                """
            SELECT
                elem->>'entity_type' AS entity_type,
                COUNT(*) AS count_
            FROM content_analysis,
            LATERAL json_array_elements(analysis_metadata->'results') AS elem
            WHERE content_type = :content_type
            AND (elem->>'score')::float > :score_threshold
            GROUP BY entity_type
            ORDER BY count_ DESC
            LIMIT :top;
            """
            )

            result = session.execute(
                sql, {"content_type": "text/plain", "score_threshold": score_threshold, "top": top}
            )
            return {row.entity_type: row.count_ for row in result}

    def pii_detected_rate(self) -> float:
        with self.db() as session:
            total_count = session.query(func.count()).filter(DBContentAnalysis.content_type == "text/plain").scalar()

            pii_count = (
                session.query(func.count())
                .filter(
                    DBContentAnalysis.content_type == "text/plain",
                    func.json_array_length(DBContentAnalysis.analysis_metadata["results"]) > 0,
                )
                .scalar()
            )

            if total_count == 0:
                return 0.0

            rate = (pii_count / total_count) * 100.0
            return rate

    def get_content_insights(self) -> ContentInsight:
        """Get insights on content toxicity and PII detection."""
        return ContentInsight(
            most_common_toxicity_labels=self.most_common_toxicity_label(),
            most_common_pii_types=self.most_common_pii_types(),
            pii_detected_rate=self.pii_detected_rate(),
        )

    def get_dashboard_summary(self) -> DashboardSummary:
        """Get the complete dashboard summary."""
        content_summary = self.get_content_volume_and_flow()
        moderation_summary = self.moderation_outcomes()
        insights = self.get_content_insights()

        return DashboardSummary(content=content_summary, moderation=moderation_summary, insights=insights)


# PII Detected Rate	% of submissions containing any PII
# Most Common PII Types
