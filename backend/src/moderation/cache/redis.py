import json
import logging
from dataclasses import dataclass

import redis
from moderation.core.settings import settings
from redis import Redis

logger = logging.getLogger(__name__)


@dataclass
class ClientAccess:
    # "user_id": str(client.id),
    #                     "source": client.source,
    #                     "scopes": client.current_scope,
    #                     "is_active": client.is_active,
    #                     "access_count": client.access_count,
    user_id: str
    source: str
    scopes: list
    is_active: bool
    access_count: int


class RedisClient(Redis):
    def get_client_access(self, key: str) -> ClientAccess | None:
        key_ = f"{settings.REDIS_API_KEY_PREFIX}:{key}"
        try:
            response = self.get(key_)
            if response is None:
                return None
            client = json.loads(response)
            return ClientAccess(
                user_id=client["user_id"],
                source=client["source"],
                scopes=client["scopes"],
                is_active=client["is_active"],
                access_count=client["access_count"],
            )
        except (json.JSONDecodeError, KeyError):
            logger.critical(f"Corrupted data in Redis for key: {key}")
            raise redis.exceptions.ResponseError("Corrupted data in Redis")


def get_redis_client() -> RedisClient:
    return RedisClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
