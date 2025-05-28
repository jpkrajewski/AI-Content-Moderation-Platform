import logging
from typing import Callable, ContextManager, List, Optional

from moderation.db.analysis import ContentAnalysis as DBContentAnalysis
from moderation.repository.db.analysis.base import AbstractAnalysisRepository, AnalysisResult
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DatabaseAnalysisRepository(AbstractAnalysisRepository):
    """Database-backed implementation of the analysis repository."""

    def __init__(self, db: Callable[[], ContextManager[Session]]) -> None:
        """Initialize the repository with a database session context factory."""
        self.db = db

    def save_result(self, content_id: str, result: AnalysisResult) -> Optional[DBContentAnalysis]:
        """Save a new analysis result to the database and return the saved record."""
        logger.info(f"Saving analysis result for content ID {content_id}: {result}")
        stmt = (
            insert(DBContentAnalysis)
            .values(
                content_id=content_id,
                content_type=result.content_type,
                automated_flag=result.automated_flag,
                automated_flag_reason=result.automated_flag_reason,
                model_version=result.model_version,
                analysis_metadata=result.analysis_metadata,
                filename=result.filename,
            )
            .returning(DBContentAnalysis)  # return all columns of the inserted row
        )

        try:
            with self.db() as session:
                result_proxy = session.execute(stmt)
                inserted_record = result_proxy.fetchone()
                session.commit()
                return inserted_record  # This will be a DBContentAnalysis instance (if mapped correctly)
        except SQLAlchemyError:
            logger.exception("Failed to save analysis result.")
            session.rollback()
            return None

    def save_result_bulk(self, content_id: str, results: List[AnalysisResult]) -> bool:
        """Save multiple analysis results to the database in bulk."""
        logger.info(f"Saving bulk analysis results for content ID {content_id}: {len(results)} results")

        # Prepare the list of dictionaries for bulk insert
        values = [
            {
                "content_id": content_id,
                "content_type": result.content_type,
                "automated_flag": result.automated_flag,
                "automated_flag_reason": result.automated_flag_reason,
                "model_version": result.model_version,
                "analysis_metadata": result.analysis_metadata,
                "filename": result.filename,
            }
            for result in results
        ]

        stmt = insert(DBContentAnalysis).values(values)

        try:
            with self.db() as session:
                session.execute(stmt)
                session.commit()
                logger.info(f"Successfully saved {len(results)} analysis results for content ID {content_id}")
                return True
        except SQLAlchemyError:
            logger.exception("Failed to save bulk analysis results.")
            session.rollback()
            return False

    def get_results(self, content_id: str) -> list[AnalysisResult] | None:
        """Retrieve all analysis results for a given content ID."""
        with self.db() as session:
            results = session.query(DBContentAnalysis).filter(DBContentAnalysis.content_id == content_id).all()
            if not results:
                return None
            return [
                AnalysisResult(
                    content_id=result.content_id,
                    content_type=result.content_type,
                    automated_flag=result.automated_flag,
                    automated_flag_reason=result.automated_flag_reason,
                    model_version=result.model_version,
                    analysis_metadata=result.analysis_metadata,
                    filename=result.filename,
                )
                for result in results
            ]

    def delete_result(self, content_id: str) -> bool:
        """Delete all analysis results for a given content ID."""
        with self.db() as session:
            try:
                session.query(DBContentAnalysis).filter(DBContentAnalysis.content_id == content_id).delete()
                session.commit()
                return True
            except SQLAlchemyError:
                logger.exception("Failed to delete analysis result.")
                session.rollback()
                return False

    def list_results(self) -> list[AnalysisResult]:
        """List all analysis results in the database."""
        with self.db() as session:
            results = session.query(DBContentAnalysis).all()
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
        """Update an analysis result. (Unimplemented placeholder)."""
        return False
