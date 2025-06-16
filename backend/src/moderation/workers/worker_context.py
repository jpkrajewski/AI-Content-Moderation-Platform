import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, ContextManager

from moderation.db import get_db
from moderation.repository.db.analysis.database import DatabaseAnalysisRepository
from moderation.repository.db.content.database import DatabaseContentRepository
from moderation.service.analysis import AnalysisService
from moderation.service.content.content_service import ContentService
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class WorkerContext:
    def __init__(self, db: Callable[[], ContextManager[Session]] | None = None) -> None:
        self.db = db or get_db
        self.content_service = self.get_content_service()
        self.analysis_service = self.get_analysis_service()
        self.content_repository = DatabaseContentRepository(db=self.db)
        self.analysis_repository = DatabaseAnalysisRepository(db=self.db)

    def get_content_service(self) -> ContentService:
        return ContentService(
            analysis_repository=DatabaseAnalysisRepository(
                db=self.db,
            ),
            content_repository=DatabaseContentRepository(
                db=self.db,
            ),
        )

    def get_analysis_service(self) -> AnalysisService:
        return AnalysisService(
            analysis_repository=DatabaseAnalysisRepository(
                db=self.db,
            )
        )

    def __enter__(self) -> "WorkerContext":
        return self

    def __exit__(self, exc_type_, exc_val_, exc_tb_):
        pass


@asynccontextmanager
async def get_worker_context() -> AsyncGenerator[WorkerContext, Any]:
    logger.info("Starting worker context")

    try:
        with WorkerContext(
            db=get_db,
        ) as worker_context:
            yield worker_context

    except Exception as ex:
        logger.exception(ex)
        raise ex

    finally:
        logger.info("Worker context closed.")
