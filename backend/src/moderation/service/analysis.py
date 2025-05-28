from typing import List

from moderation.repository.db.analysis.base import AbstractAnalysisRepository, AnalysisResult


class AnalysisService:
    def __init__(self, analysis_repository: AbstractAnalysisRepository) -> None:
        self.repository = analysis_repository

    def save_result(self, content_id: str, result: AnalysisResult) -> bool:
        """Save the moderation result to the database."""
        return self.repository.save_result(content_id, result)

    def save_analysis_result_bulk(self, content_id: str, results: List[AnalysisResult]) -> bool:
        """Save the moderation result to the database."""
        return self.repository.save_result_bulk(content_id, results)
