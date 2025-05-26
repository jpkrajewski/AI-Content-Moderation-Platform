import json
import logging
from dataclasses import asdict, is_dataclass
from functools import cache, wraps
from typing import Any, Callable, Union, get_args, get_origin, get_type_hints

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


def unwrap_optional(t):
    """Unwrap Optional[Dataclass] or Union[Dataclass, None]."""
    if get_origin(t) is Union:
        non_none = [arg for arg in get_args(t) if arg is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return t


def cached_dataclass(prefix: str, suffix_attr: str):
    def decorator(func: Callable):
        ret_type = unwrap_optional(get_type_hints(func).get("return"))

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None or not is_dataclass(result):
                return result

            suffix = getattr(result, suffix_attr, None)
            if not suffix:
                return result

            key = f"{prefix}:{suffix}"
            client = get_redis_client()

            # Attempt to fetch from cache
            cached = client.get(key)
            if cached:
                try:
                    data = json.loads(cached)
                    if is_dataclass(ret_type):
                        return ret_type(**data)
                    return data
                except Exception as e:
                    logger.warning(f"Deserialization error for key {key}: {e}")

            # Cache the fresh result
            try:
                client.set(key, json.dumps(asdict(result)))
            except Exception as e:
                logger.error(f"Error caching result for {func.__name__}: {e}")

            return result

        return wrapper

    return decorator
