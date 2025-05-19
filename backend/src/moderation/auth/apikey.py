import logging

from moderation.cache.redis import get_redis_client

logger = logging.getLogger(__name__)

# This connects to the Redis container by its service name
redis_client = get_redis_client()


def apikey_auth(key: str, required_scopes: list):
    # client_data = redis_client.get_client_access(key)
    # if client_data is None:
    #     raise ClientProblem(title="Invalid API key")
    # check_scopes(client_data.scopes, required_scopes)
    # return {"sub": client_data.user_id, "scopes": client_data.scopes}
    return {"sub": "test_user", "scopes": ["moderation"]}  # TODO: remove this line
