from moderation.models.classification import Result


class TagResult:
    def __init__(self, tag: str):
        self.tag = tag

    def __call__(self, result: Result) -> Result:
        result.content_type = f"{self.tag}/{result.content_type}"
        return result


class ResultExcludeEmpty:
    def __call__(self, result: Result) -> Result | None:
        if not result.analysis_metadata["results"]:
            return None
        return result
