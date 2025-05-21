from functools import cache

from moderation.ai.models import PIIResult
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


@cache
def get_analyzer() -> AnalyzerEngine:
    return AnalyzerEngine()


@cache
def get_anonymizer() -> AnonymizerEngine:
    return AnonymizerEngine()


class PIIAnalyzer:
    def __init__(self, analizer: AnalyzerEngine, anonymizer: AnonymizerEngine) -> None:
        self.analyzer = analizer
        self.anonymizer = anonymizer

    def analyze(self, text: str) -> PIIResult:
        results = self.analyzer.analyze(text=text, language="en")
        return PIIResult(
            content_type="text/plain",
            results=results,
            model_version="",
        )

    def anonymize(self, text: str, analyzer_results: list) -> str:
        anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
        return anonymized_text


@cache
def get_pii_analyzer() -> PIIAnalyzer:
    analyzer = get_analyzer()
    anonymizer = get_anonymizer()
    return PIIAnalyzer(analyzer, anonymizer)
