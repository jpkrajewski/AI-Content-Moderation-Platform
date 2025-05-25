import json
import logging

from connexion.exceptions import Unauthorized
from moderation.auth.common import check_scopes
from moderation.cache.redis import get_redis_client
from moderation.constants.general import REDIS_CLIENT_API_KEY
from moderation.service import get_client_api_key_service
from moderation.service.client_api_key import ClientApiKey
from pydantic import ValidationError

logger = logging.getLogger(__name__)
redis_client = get_redis_client()


def deserialize_client_api_key(data: str) -> ClientApiKey | None:
    """Attempt to deserialize JSON into a ClientApiKey object."""
    try:
        return ClientApiKey(**json.loads(data))
    except ValidationError as e:
        logger.error(f"Invalid API key data in cache: {e}")
        return None


def get_client_api_key(key: str) -> ClientApiKey | None:
    """Retrieve API key from cache or fallback to DB."""
    cache_key = f"{REDIS_CLIENT_API_KEY}:{key}"

    cached = redis_client.get(cache_key)
    if cached:
        client_api_key = deserialize_client_api_key(cached)
        if client_api_key:
            return client_api_key

    # Fallback to DB
    client_api_key = get_client_api_key_service().get_by_api_key(key)
    if client_api_key:
        redis_client.set(cache_key, json.dumps(client_api_key.to_dict()))
    return client_api_key


def apikey_auth(key: str, required_scopes: list[str]) -> dict:
    """Main authentication function for API key."""
    client_api_key = get_client_api_key(key)
    if not client_api_key:
        logger.warning(f"API key not found or invalid: {key}")
        raise Unauthorized()

    check_scopes(client_api_key.current_scope, required_scopes)
    return {
        "sub": client_api_key.client_id,
        "scopes": client_api_key.current_scope,
    }
