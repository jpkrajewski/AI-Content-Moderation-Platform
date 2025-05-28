from dataclasses import dataclass
from typing import List

from presidio_analyzer.recognizer_result import RecognizerResult


@dataclass
class Result:
    content_type: str
    model_version: str
    analysis_metadata: dict
    automated_flag: bool | None = None
    automated_flag_reason: str | None = None

    @classmethod
    def from_pii(cls, model_version: str, results: List[RecognizerResult]) -> "Result":
        return cls(
            content_type="pii",
            model_version=model_version,
            analysis_metadata={
                "results": [
                    {
                        "entity_type": result.entity_type,
                        "start": result.start,
                        "end": result.end,
                        "score": result.score,
                    }
                    for result in results
                ]
            },
        )

    @classmethod
    def from_google_safe_websearch(cls, model_version: str, results: List[dict]) -> "Result":
        return cls(content_type="url", model_version=model_version, analysis_metadata={"results": results})
