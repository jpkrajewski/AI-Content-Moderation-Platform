import logging
from typing import List, Union, Dict
import httpx
import asyncio

logger = logging.getLogger(__name__)

class AsyncGoogleSafeBrowsingClient:
    BASE_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    THREAT_TYPES = [
        "MALWARE",
        "SOCIAL_ENGINEERING",
        "UNWANTED_SOFTWARE",
        "POTENTIALLY_HARMFUL_APPLICATION",
    ]

    def __init__(self, api_key: str, client_id: str = "yourcompanyname", client_version: str = "1.0") -> None:
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        self.client_info = {
            "clientId": client_id,
            "clientVersion": client_version,
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
            return {"url": url, "error": str(e)}

        data = response.json()
        if "matches" in data:
            logger.warning(f"Unsafe URL detected: {url} - Details: {data['matches']}")
            return {"url": url, "safe": False, "details": data["matches"]}
        logger.info(f"URL is safe: {url}")
        return {"url": url, "safe": True, "details": None}

    async def check_urls(self, urls: List[str]) -> List[Dict[str, Union[str, dict, bool]]]:
        async with httpx.AsyncClient() as client:
            tasks = [self.check_url(client, url) for url in urls]
            return await asyncio.gather(*tasks)
