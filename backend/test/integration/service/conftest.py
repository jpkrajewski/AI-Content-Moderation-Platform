import os
from unittest.mock import patch

import pytest
from moderation.db.base import Base
from moderation.db.session import engine, get_db
from moderation.repository.db.client_api_key.database import DatabaseClientApiKeyRepository
from moderation.service.apikey.apikeys_service import ClientApiKeyService
from sqlalchemy import create_engine, text


@pytest.fixture(autouse=True)
def disable_cache_decorator():
    with patch(
        "moderation.service.client_api_key.cached_dataclass",
        lambda *args, **kwargs: lambda fn: fn,
    ):
        yield


@pytest.fixture(autouse=True)
def mock_redis():
    with patch("moderation.cache.redis.Redis") as mock:
        yield mock


@pytest.fixture(scope="session", autouse=True)
def create_schema():
    db_user = os.getenv("DB_USER", "test_postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5433")
    db_name = os.getenv("DB_NAME", "moderation_db")

    base_db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
    base_engine = create_engine(base_db_url, isolation_level="AUTOCOMMIT")

    with base_engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :dbname"), {"dbname": db_name})
        if not result.scalar():
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"✅ Created database {db_name}")

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def client_api_key_service():
    return ClientApiKeyService(
        api_key_repository=DatabaseClientApiKeyRepository(db=get_db),
    )
