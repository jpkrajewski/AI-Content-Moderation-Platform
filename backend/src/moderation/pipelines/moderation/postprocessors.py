from typing import Any

from moderation.models.classification import Result


class TagResult:
    def __init__(self, tag: str):
        self.tag = tag

    def __call__(self, result: Result) -> Result:
        result.content_type = f"{self.tag}/{result.content_type}"
        return result


class ResultExcludeEmptyMetadata:
    def __call__(self, result: Result) -> Result | None:
        if not result.analysis_metadata["results"]:
            return None
        return result


class ReturnSame:
    def __call__(self, result: Any) -> Any:
        return result


class ResultExcludeNotFlagged:
    def __call__(self, result: Result) -> Result | None:
        if not result.automated_flag:
            return None
        return result
