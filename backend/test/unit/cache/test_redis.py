import json
from dataclasses import asdict, dataclass
from typing import Optional
from unittest.mock import MagicMock, patch

from moderation.cache.redis import cached_dataclass


@dataclass
class FakeUser:
    id: str
    name: str


@cached_dataclass(prefix="test", suffix_attr="id")
def get_user(user_id: str) -> Optional[FakeUser]:
    if user_id == "none":
        return None
    return FakeUser(id=user_id, name="John")


def test_cache_saves_dataclass_result():
    mock_redis = MagicMock()

    with patch("moderation.cache.redis.get_redis_client", return_value=mock_redis):
        result = get_user("123")
        assert isinstance(result, FakeUser)

        # Confirm cache set called with correct key and JSON string of dataclass dict
        expected_key = "test:123"
        expected_value = json.dumps(asdict(result))
        mock_redis.set.assert_called_once_with(expected_key, expected_value)


def test_cache_skips_none_result():
    mock_redis = MagicMock()

    with patch("moderation.cache.redis.get_redis_client", return_value=mock_redis):
        result = get_user("none")
        assert result is None
        mock_redis.set.assert_not_called()


def test_cache_reads_from_redis_if_available():
    fake_user = FakeUser(id="456", name="Cached")
    mock_redis = MagicMock()

    # Serialize FakeUser as JSON string
    cached_json = json.dumps(asdict(fake_user))
    mock_redis.get.return_value = cached_json.encode("utf-8")  # Redis returns bytes

    with patch("moderation.cache.redis.get_redis_client", return_value=mock_redis):
        result = get_user("456")
        assert isinstance(result, FakeUser)
        assert result == fake_user
        mock_redis.get.assert_called_once_with("test:456")


def test_cache_fallback_on_deserialize_error():
    mock_redis = MagicMock()
    # corrupted JSON data
    mock_redis.get.return_value = b"not-a-json"

    with patch("moderation.cache.redis.get_redis_client", return_value=mock_redis):
        result = get_user("789")
        # fallback returns the function's actual returned dataclass instance
        assert isinstance(result, FakeUser)
        assert result.id == "789"
        # It should save the valid fresh data back to cache after fallback
        mock_redis.set.assert_called_once()
