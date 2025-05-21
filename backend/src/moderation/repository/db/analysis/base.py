from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    content_id: str
    content_type: str
    automated_flag: bool
    automated_flag_reason: str
    model_version: str
    analysis_metadata: dict
    filename: str | None = None


class AbstractAnalysisRepository(ABC):
    @abstractmethod
    def save_result(self, content_id: str, result: AnalysisResult) -> bool:
        """Save the moderation result to the database."""

    @abstractmethod
    def get_results(self, content_id: str) -> list[AnalysisResult] | None:
        """Retrieve the moderation result from the database."""

    @abstractmethod
    def delete_result(self, content_id: str) -> bool:
        """Delete the moderation result from the database."""

    @abstractmethod
    def list_results(self) -> list[AnalysisResult]:
        """List all moderation results."""

    @abstractmethod
    def update_result(self, content_id: str, result: AnalysisResult) -> bool:
        """Update the moderation result in the database."""
