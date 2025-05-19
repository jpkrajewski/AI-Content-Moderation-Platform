import logging

from moderation.db.analysis import ContentAnalysis as DBContentAnalysis
from moderation.repository.db.analysis.base import AbstractAnalysisRepository, AnalysisResult
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DatabaseAnalysisRepository(AbstractAnalysisRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_result(self, content_id: str, result: AnalysisResult) -> bool:

        record = DBContentAnalysis(
            content_id=content_id,
            content_type=result.content_type,
            automated_flag=result.automated_flag,
            automated_flag_reason=result.automated_flag_reason,
            model_version=result.model_version,
            analysis_metadata=result.analysis_metadata,
        )

        self.session.add(record)
        try:
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False
        return False

    def get_results(self, content_id: str) -> list[AnalysisResult] | None:
        results = self.session.query(DBContentAnalysis).filter(DBContentAnalysis.content_id == content_id)
        return (
            [
                AnalysisResult(
                    content_id=result.content_id,
                    content_type=result.content_type,
                    automated_flag=result.automated_flag,
                    automated_flag_reason=result.automated_flag_reason,
                    model_version=result.model_version,
                    analysis_metadata=result.analysis_metadata,
                )
                for result in results
            ]
            if results
            else None
        )

    def delete_result(self, content_id: str) -> bool:
        self.session.query(DBContentAnalysis).filter(DBContentAnalysis.content_id == content_id).delete()
        try:
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False
        return False

    def list_results(self) -> list[AnalysisResult]:
        results = self.session.query(DBContentAnalysis).all()
        logger.debug(f"Fetched {len(results)} results from the database.")
        return [
            AnalysisResult(
                content_id=result.content_id,
                content_type=result.content_type,
                automated_flag=result.automated_flag,
                automated_flag_reason=result.automated_flag_reason,
                model_version=result.model_version,
                analysis_metadata=result.analysis_metadata,
            )
            for result in results
        ]

    def update_result(self, content_id: str, result: AnalysisResult) -> bool:
        return False
