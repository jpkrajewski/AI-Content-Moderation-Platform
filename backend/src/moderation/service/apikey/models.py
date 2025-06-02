from dataclasses import dataclass

@dataclass
class GenericApiKeyInfo:
    active_count: int
    deactivated_count: int
    all_count: int