from moderation.repository.db.analysis.base import AbstractAnalysisRepository, AnalysisResult


class AnalysisService:
    def __init__(self, repository: AbstractAnalysisRepository) -> None:
        self.repository = repository

    def save_result(self, content_id: str, result: AnalysisResult) -> bool:
        """Save the moderation result to the database."""
        return self.repository.save_result(content_id, result)
