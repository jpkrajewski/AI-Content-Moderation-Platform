# bandit: skip=B105
import json
import logging
import time

import redis
from moderation.cache.redis import get_redis_client
from moderation.core.settings import settings
from moderation.db.access import ClientAccess
from moderation.db.session import get_db

logger = logging.getLogger(__name__)


def load_clients_into_redis(max_retries=5, retry_delay=2):
    for attempt in range(max_retries):
        try:
            redis_client = get_redis_client()
            # Test the connection
            redis_client.ping()
            logger.info("Connected to Redis successfully")
            break
        except redis.exceptions.ConnectionError as e:
            logger.warning(f"Attempt {attempt+1}: Redis connection failed: {e}")
            time.sleep(retry_delay)
    else:
        logger.error("Could not connect to Redis after multiple retries.")
        return

    try:
        with get_db() as session:
            clients = session.query(ClientAccess).filter_by(is_active=True).all()
        with redis_client.pipeline(transaction=True) as pipe:
            for client in clients:
                key = f"{settings.REDIS_API_KEY_PREFIX}:{client.api_key}"
                value = json.dumps(
                    {
                        "user_id": str(client.id),
                        "source": client.source,
                        "scopes": client.current_scope,
                        "is_active": client.is_active,
                        "access_count": client.access_count,
                    }
                )
                # Overwrite key atomically
                pipe.set(key, value)
            pipe.execute()
        logger.info(f"Loaded {len(clients)} client keys into Redis.")
    except Exception as e:
        logger.exception(f"Failed to load API keys into Redis: {e}")
