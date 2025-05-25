import json
import logging
from dataclasses import asdict, is_dataclass
from functools import cache
from typing import Any

from moderation.core.settings import settings
from pydantic import BaseModel
from redis import Redis

logger = logging.getLogger(__name__)


@cache
def get_redis_client() -> Redis:
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


def try_serialize(obj: Any) -> dict | list | None:
    """Attempt to serialize an object to JSON-compatible data, or return None on failure."""
    if is_dataclass(obj):
        obj = asdict(obj)
    elif isinstance(obj, BaseModel):
        obj = obj.model_dump()
    if isinstance(obj, (list, tuple)):
        return [try_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: try_serialize(v) for k, v in obj.items()}
    else:
        try:
            json.dumps(obj)  # Check if it can be serialized
        except (TypeError, ValueError):
            logger.warning(f"Object of type {type(obj)} cannot be serialized to JSON.")
            return None
    return obj


def pop(kwargs: dict, user: bool = True, token: bool = True):
    """
    Connexion adds 'user' and 'token_info' to kwargs if JWT auth is used.
    Since we pass **kwargs in wrappers, every route ends up with them — even if not needed.
    This just pops them so routes don’t have to care.
    """
    if user:
        kwargs.pop("user", None)
    if token:
        kwargs.pop("token_info", None)
    return kwargs


def cached_response(key: str | None = None, pop_user: bool = True, pop_token: bool = True):
    """Decorator to cache function results in Redis."""

    def inner(func):
        def wrapper(*args, **kwargs):
            client = get_redis_client()
            if key is not None:
                cache_key = f"{key}:{kwargs.get('user', '')}"
            else:
                cache_key = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"

            cached_result = client.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for {cache_key}")
                data = json.loads(cached_result)
                return data["result"], data["status"]

            logger.info(f"Cache miss for {cache_key}")
            result, status = func(*args, **pop(kwargs, user=pop_user, token=pop_token))
            serialized_result = try_serialize(result)
            client.set(cache_key, json.dumps({"result": serialized_result, "status": status}), ex=300)
            return serialized_result, status

        return wrapper

    return inner


def invalidate_cache(key: str, pop_user: bool = True, pop_token: bool = True):
    def inner(func):
        """Decorator to invalidate cache for a function."""

        def wrapper(*args, **kwargs):
            client = get_redis_client()
            cache_key = f"{key}:{kwargs['user']}"
            client.delete(cache_key)
            logger.info(f"Cache invalidated for {cache_key}")
            pop(kwargs, pop_user, token=pop_token)
            logger.debug(f"Function arguments: args={args}, kwargs={kwargs}")
            return func(*args, **pop(kwargs, user=pop_user, token=pop_token))

        return wrapper

    return inner


def update_cached_repository_single_result(
    prefix: str,
    obj_identifier_attribute: str,
):
    def inner(func):
        def wrapper(*args, **kwargs):
            client = get_redis_client()
            result = func(*args, **kwargs)
            serialized_result = try_serialize(result)
            cache_key = f"{prefix}:{serialized_result[obj_identifier_attribute]}"
            client.set(
                cache_key,
                serialized_result,
            )
            return result

        return wrapper

    return inner
