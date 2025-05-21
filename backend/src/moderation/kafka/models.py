from dataclasses import dataclass


@dataclass
class KafkaModerationMessage:
    content_id: str
    type: str
    message: str
    filename: str | None = None
    filepath: str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            content_id=data["content_id"],
            type=data["type"],
            message=data["message"],
            filename=data.get("filename"),
            filepath=data.get("filepath"),
        )

    def validate(self) -> None:
        if self.type not in ["text", "image", "document"]:
            raise ValueError(f"Invalid type: {self.type}")

    def get_input_data(self) -> str:
        if self.type == "text":
            return self.message
        if self.filepath is None:
            raise ValueError("File path is required for image or document types")
        return self.filepath

    def is_text(self) -> bool:
        return self.type == "text"
