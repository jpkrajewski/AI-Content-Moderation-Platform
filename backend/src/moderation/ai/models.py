from dataclasses import dataclass

from presidio_analyzer.recognizer_result import RecognizerResult


@dataclass
class ClassifyResult:
    content_type: str
    automated_flag: bool
    automated_flag_reason: str
    model_version: str
    analysis_metadata: dict


@dataclass
class PIIResult:
    content_type: str
    results: list[RecognizerResult]
    model_version: str

    def get_analysis_metadata(self) -> dict:
        return {
            "results": [
                {
                    "entity_type": result.entity_type,
                    "start": result.start,
                    "end": result.end,
                    "score": result.score,
                }
                for result in self.results
            ]
        }
