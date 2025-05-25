import json
import logging

from connexion.exceptions import Unauthorized
from moderation.auth.common import check_scopes
from moderation.cache.redis import get_redis_client
from moderation.constants.cache import REDIS_CLIENT_API_KEY
from moderation.service import get_client_api_key_service
from moderation.service.client_api_key import ClientApiKey
from pydantic import ValidationError
from redis import Redis

logger = logging.getLogger(__name__)

# This connects to the Redis container by its service name
redis_client = get_redis_client()


def get_client_api_key_from_cache(redis: Redis, api_key: str) -> ClientApiKey | None:
    result = redis.get(f"{REDIS_CLIENT_API_KEY}:{api_key}")
    if result is None:
        return None
    try:
        return ClientApiKey(**json.loads(result))
    except ValidationError as e:
        logger.error(f"Failed to validate API key {api_key}: {e}")
        return None


def apikey_auth(key: str, required_scopes: list[str]) -> dict:
    client_api_key = get_client_api_key_from_cache(redis_client, key)
    if client_api_key is None:
        client_api_key = get_client_api_key_service().get_by_api_key(key)
        if client_api_key is None:
            raise Unauthorized()
        redis_client.set(f"{REDIS_CLIENT_API_KEY}:{key}", json.dumps(client_api_key.to_dict()))
    check_scopes(client_api_key.current_scope, required_scopes)
    return {"sub": client_api_key.client_id, "scopes": client_api_key.current_scope}
