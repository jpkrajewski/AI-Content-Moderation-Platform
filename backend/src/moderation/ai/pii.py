from functools import cache

from presidio_analyzer.nlp_engine import NlpEngineProvider

from moderation.models.classification import Result
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine


@cache
def get_analyzer() -> AnalyzerEngine:
    nlp_config = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_md"}]
    }

    provider = NlpEngineProvider(nlp_configuration=nlp_config)
    nlp_engine = provider.create_engine()

    return AnalyzerEngine(nlp_engine=nlp_engine)


@cache
def get_anonymizer() -> AnonymizerEngine:
    return AnonymizerEngine()


class PIIAnalyzer:
    def __init__(self, analizer: AnalyzerEngine, anonymizer: AnonymizerEngine) -> None:
        self.analyzer = analizer
        self.anonymizer = anonymizer

    def analyze(self, text: str) -> Result:
        results = self.analyzer.analyze(text=text, language="en")
        return Result.from_pii(
            model_version=self.analyzer.nlp_engine.engine_name,
            results=results,
        )

    def anonymize(self, text: str, analyzer_results: list) -> str:
        anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
        return anonymized_text


@cache
def get_pii_analyzer() -> PIIAnalyzer:
    analyzer = get_analyzer()
    anonymizer = get_anonymizer()
    return PIIAnalyzer(analyzer, anonymizer)
