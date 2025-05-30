from typing import Any, Dict, List, Optional
from uuid import UUID

from moderation.repository.db.analysis.base import AbstractAnalysisRepository, AnalysisResult
from moderation.repository.db.content.base import (
    AbstractDBContentRepository,
    Content,
    ContentWithAnalysis,
    content_with_analysis,
)
from moderation.service.content.models import GenericContentInfo


class ContentService:
    """Service layer that coordinates between API endpoints and database."""

    def __init__(
        self,
        content_repository: AbstractDBContentRepository,
        analysis_repository: AbstractAnalysisRepository,
    ):
        self.content_repository = content_repository
        self.analysis_repository = analysis_repository

    def create_content(
        self,
        input: Dict[str, Any],
        image_paths: List[str],
        document_paths: List[str],
        video_paths: List[str],
        audio_paths: List[str],
    ) -> Content:
        try:
            content = Content(
                user_id=input["user_id"],
                username=input["username"],
                title=input["title"],
                body=input["body"],
                tags=input["tags"],
                localization=input["localization"],
                source=input["source"],
                image_paths=image_paths,
                document_paths=document_paths,
                video_paths=video_paths,
                audio_paths=audio_paths,
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e.args[0]}")
        return self.content_repository.create(content)

    def list_content(self, status: Optional[str] = None) -> List[Content]:
        return self.content_repository.list(status)

    def get_content(self, content_id: str) -> Content:
        content = self.content_repository.get_by_id(content_id)
        if not content:
            raise ValueError("Content not found")
        return content

    def update_content(self, content_id: str, data: Content) -> Content:
        updated = self.content_repository.update(content_id, data)
        if not updated:
            raise ValueError("Content not found")
        return updated

    def update_content_status(self, content_id: str, user: UUID, status: str) -> Content:
        updated = self.content_repository.update_status(content_id, user, status)
        if not updated:
            raise ValueError("Content not found")
        return updated

    def delete_content(self, content_id: str) -> None:
        success = self.content_repository.delete(content_id)
        if not success:
            raise ValueError("Content not found")

    def save_analysis_result(self, content_id: str, result: AnalysisResult) -> None:
        saved = self.analysis_repository.save_result(content_id, result)
        if not saved:
            raise RuntimeError("Failed to save analysis result")
        return saved

    def save_result_bulk(self, content_id: str, results: List[AnalysisResult]) -> None:
        saved = self.analysis_repository.save_result_bulk(content_id, results)
        if not saved:
            raise RuntimeError("Failed to save analysis result")

    def get_analysis_result(self, content_id: str) -> ContentWithAnalysis:
        content = self.content_repository.get_by_id(content_id)
        if not content:
            raise ValueError("Content not found")

        results = self.analysis_repository.get_results(content_id)
        if not results:
            raise ValueError("Analysis results not found")

        return content_with_analysis(content, results)

    def list_pending(self, page: int = 1, page_size: int = 10) -> List[ContentWithAnalysis]:
        """
        List pending content with pagination.

        Args:
            page (int): The page number to retrieve (1-based index).
            page_size (int): The number of items per page.

        Returns:
            List[ContentWithAnalysis]: A list of content with analysis for the specified page.

        Raises:
            ValueError: If no pending content is found.
        """
        # Calculate the offset and limit for pagination
        offset = (page - 1) * page_size
        limit = page_size

        # Fetch the paginated list of pending content
        return self.content_repository.list_with_analysis(status="pending", offset=offset, limit=limit)

    def get_info(self) -> GenericContentInfo:
        pending_count = self.content_repository.count(status="pending")
        return GenericContentInfo(
            pending_count=pending_count,
        )
