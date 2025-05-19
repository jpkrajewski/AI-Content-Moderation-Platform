from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple

from moderation.repository.db.analysis.base import AbstractAnalysisRepository
from moderation.repository.db.analysis.base import AnalysisResult as DBAnalysisResult
from moderation.repository.db.content.base import AbstractDBContentRepository, Content


@dataclass
class AnalysisResult:
    content_type: str
    automated_flag: bool
    automated_flag_reason: str
    model_version: str
    analysis_metadata: Dict[str, Any]


@dataclass
class ContentWithAnalysis:
    body: str
    tags: List[str]
    localization: str
    source: str
    status: str
    created_at: str
    results: List[AnalysisResult]


def content_with_analysis(content: Content, results: List[DBAnalysisResult]) -> ContentWithAnalysis:
    """Combine content and analysis results into a single object."""
    return ContentWithAnalysis(
        body=content.body,
        tags=content.tags,
        localization=content.localization,
        source=content.source,
        status=content.status,
        created_at=content.created_at.isoformat() if content.created_at else None,
        results=[
            AnalysisResult(
                content_type=result.content_type,
                automated_flag=result.automated_flag,
                automated_flag_reason=result.automated_flag_reason,
                model_version=result.model_version,
                analysis_metadata=result.analysis_metadata,
            )
            for result in results
        ],
    )


class ContentService:
    """Service layer that coordinates between API endpoints and database."""

    def __init__(
        self, content_repository: AbstractDBContentRepository, analysis_repository: AbstractAnalysisRepository
    ):
        self.content_repository = content_repository
        self.analysis_repository = analysis_repository

    def create_content(self, input: Dict[str, Any], image_paths: List[str]) -> Content:
        """Create new content and queue it for moderation."""
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
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        return self.content_repository.create(content)

    def list_content(self, status: Optional[str] = None) -> Tuple[List[Content], HTTPStatus]:
        """List all content with optional status filter."""
        content_list = self.content_repository.list(status)
        return content_list, HTTPStatus.OK

    def get_content(self, content_id: str) -> Tuple[Content, HTTPStatus]:
        """Get specific content by ID."""
        content = self.content_repository.get_by_id(content_id)
        if content:
            return content, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def update_content(self, content_id: str, data: Content) -> Tuple[Content, HTTPStatus]:
        """Update content properties."""
        content = self.content_repository.update(content_id, data)
        if content:
            return content, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def update_content_status(self, content_id: str, status: str) -> Tuple[Content, HTTPStatus]:
        """Update content moderation status."""
        content = self.content_repository.update_status(content_id, status)
        if content:
            return content, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def delete_content(self, content_id: str) -> Tuple[Content, HTTPStatus]:
        """Delete content by ID."""
        success = self.content_repository.delete(content_id)
        if success:
            return {"message": f"Content {content_id} successfully deleted"}, HTTPStatus.OK
        return {"error": "Content not found"}, HTTPStatus.NOT_FOUND

    def save_analysis_result(self, content_id: str, result: AnalysisResult) -> Tuple[Dict[str, Any], HTTPStatus]:
        """Save analysis result for a specific content."""
        try:
            analysis_result = self.analysis_repository.save_result(content_id, result)
            if analysis_result:
                return {"message": "Analysis result saved successfully"}, HTTPStatus.OK
            return {"error": "Failed to save analysis result"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get_analysis_result(self, content_id: str) -> Tuple[ContentWithAnalysis | dict, HTTPStatus]:
        content = self.content_repository.get_by_id(content_id)
        if not content:
            return {"error": "Content not found"}, HTTPStatus.NOT_FOUND
        results = self.analysis_repository.get_results(content_id)
        if not results:
            return {"error": "Analysis result not found"}, HTTPStatus.NOT_FOUND
        return content_with_analysis(content, results), HTTPStatus.OK

    def get_analysis_result_all(self) -> Tuple[List[Dict[str, str]] | dict, HTTPStatus]:
        results = self.analysis_repository.list_results()
        if not results:
            return {"error": "No analysis results found"}, HTTPStatus.NOT_FOUND
        return [
            {
                "content_id": result.content_id,
                "content_type": result.content_type,
                "automated_flag": result.automated_flag,
                "automated_flag_reason": result.automated_flag_reason,
                "model_version": result.model_version,
                "analysis_metadata": result.analysis_metadata,
            }
            for result in results
        ], HTTPStatus.OK

    def list_pending(self) -> Tuple[list[ContentWithAnalysis] | dict[Any, Any], HTTPStatus]:
        """List all pending content."""
        content_list = self.content_repository.list()
        if not content_list:
            return {"error": "No pending content found"}, HTTPStatus.NOT_FOUND
        return [content_with_analysis(content, content.analysis) for content in content_list], HTTPStatus.OK
