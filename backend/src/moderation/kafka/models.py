from dataclasses import dataclass


@dataclass
class KafkaModerationMessage:
    content_id: str
    type: str
    message: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(content_id=data["content_id"], type=data["type"], message=data["message"])
