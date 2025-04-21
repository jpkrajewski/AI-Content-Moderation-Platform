from dataclasses import dataclass


@dataclass
class ClassifyResult:
    content_type: str
    automated_flag: bool
    autmotated_flag_reason: str
    model_version: str
    analysis_metadata: dict
