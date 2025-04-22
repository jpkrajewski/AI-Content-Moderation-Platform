from dataclasses import dataclass


@dataclass
class ClassifyResult:
    content_type: str
    automated_flag: bool
    automated_flag_reason: str
    model_version: str
    analysis_metadata: dict
