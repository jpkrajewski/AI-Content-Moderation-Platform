import asyncio
import logging
from typing import Dict, List, Union

import httpx
from moderation import MODERATION_VERSION
from moderation.core.settings import settings
from moderation.models.classification import Result

logger = logging.getLogger(__name__)


class AsyncGoogleSafeBrowsingClient:
    BASE_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    THREAT_TYPES = [
        "MALWARE",
        "SOCIAL_ENGINEERING",
        "UNWANTED_SOFTWARE",
        "POTENTIALLY_HARMFUL_APPLICATION",
    ]

    def __init__(self) -> None:
        if not settings.GOOGLE_SAFEBROWSING_CLIENT_ID:
            logger.error("GOOGLE_SAFEBROWSING_CLIENT_ID not set")

        self.api_key = settings.GOOGLE_API_KEY
        self.headers = {"Content-Type": "application/json"}
        self.client_info = {
            "clientId": settings.GOOGLE_SAFEBROWSING_CLIENT_ID,
            "clientVersion": MODERATION_VERSION,
        }

    def _prepare_payload(self, url: str) -> dict:
        return {
            "client": self.client_info,
            "threatInfo": {
                "threatTypes": self.THREAT_TYPES,
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}],
            },
        }

    async def check_url(self, client: httpx.AsyncClient, url: str) -> Dict[str, Union[str, dict, bool]]:
        try:
            response = await client.post(
                self.BASE_URL,
                headers=self.headers,
                json=self._prepare_payload(url),
                params={"key": self.api_key},
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Request to Google Safe Browsing API failed for {url}: {e}")
            return {}

        data = response.json()
        if "matches" in data:
            return {"url": url, "safe": False, "details": data["matches"]}
        return {"url": url, "safe": True, "details": {}}

    async def check_urls(self, urls: List[str]) -> Result:
        async with httpx.AsyncClient() as client:
            tasks = [self.check_url(client, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return Result.from_google_safe_websearch(
                model_version=self.BASE_URL,
                results=results,
            )
