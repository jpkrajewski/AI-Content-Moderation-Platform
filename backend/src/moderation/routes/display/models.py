from dataclasses import dataclass

from moderation.service.apikey.models import GenericApiKeyInfo
from moderation.service.content.models import GenericContentInfo


@dataclass
class UiInfo:
    contents: GenericContentInfo
    api_keys: GenericApiKeyInfo

    @classmethod
    def from_info(cls, contents: GenericContentInfo, api_keys: GenericApiKeyInfo) -> "UiInfo":
        return cls(contents=contents, api_keys=api_keys)
