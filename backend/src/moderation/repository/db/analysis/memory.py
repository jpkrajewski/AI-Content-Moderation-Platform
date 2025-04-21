from typing import Dict

from moderation.repository.db.analysis.base import AbstractAnalysisRepository, AnalysisResult


class InMemoryAnalysisRepository(AbstractAnalysisRepository):
    def __init__(self) -> None:
        self.data: Dict[str, AnalysisResult] = {}

    def save_result(self, content_id: str, result: AnalysisResult) -> bool:
        """Save the moderation result to the in-memory database."""
        self.data[content_id] = result
        return True

    def get_result(self, content_id) -> AnalysisResult | None:
        """Retrieve the moderation result from the in-memory database."""
        return self.data.get(content_id)

    def delete_result(self, content_id) -> bool:
        """Delete the moderation result from the in-memory database."""
        if content_id in self.data:
            del self.data[content_id]
            return True
        return False

    def list_results(self) -> list[AnalysisResult]:
        """List all moderation results in the in-memory database."""
        return list(self.data.values())

    def update_result(self, content_id, result) -> bool:
        """Update the moderation result in the in-memory database."""
        if content_id in self.data:
            self.data[content_id] = result
            return True
        return False
