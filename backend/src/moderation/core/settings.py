from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Content Moderation"
    ENVIRONMENT: str = "development"
    DB_URI: str = "postgresql+psycopg2://jakub:secret@db:5432/moderation_db"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    APP_RELOAD: bool = True
    APP_UPLOAD_DIR: Path = BASE_DIR / "uploads"
    APP_SECRET_KEY: str = "secret"

    # Kafka Configuration
    KAFKA_TOPIC: str = "moderation-content"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_GROUP_ID: str = "moderation-group"
    KAFKA_AUTO_OFFSET_RESET: str = "earliest"

    # Consumer Configuration
    MAX_RETRIES: int = 10
    RETRY_INTERVAL: int = 3
    KAFKA_CONSUMER_TIMEOUT_MS: int = 5000
    HEARTBEAT_INTERVAL: int = 60

    DB_REPOSITORY: Literal["memory", "database"] = "database"

    AI_AUDIO_MODEL_PATH: str = "./models/audio"
    AI_IMAGE_MODEL_PATH: str = "./models/image"
    AI_TEXT_MODEL_PATH: str = "./models/text"
    AI_IMAGE_MODEL_NAME: str = "Falconsai/nsfw_image_detection"
    AI_TEXT_MODEL_NAME: str = "unitary/toxic-bert"
    AI_AUDIO_MODEL_NAME: str = "openai/whisper-small"
    AI_IMAGE_MODERATION_THRESHOLD: float = 0.5
    AI_TEXT_MODERATION_THRESHOLD: float = 0.5

    LOGGER_CONF_PATH: Path = BASE_DIR / "logging" / "dev.conf"

    JWT_SECRET: str = "your_jwt_secret"
    JWT_ALGORITHM: str = "HS256"

    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_API_KEY_PREFIX: str = "api_key"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    GOOGLE_API_KEY: str = "your_google_api_key"
    GOOGLE_SAFEBROWSING_CLIENT_ID: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    PARSERS_VIDEO_FRAME_INTERVAL: int = 1

    FRONTEND_OAUTH_CALLBACK: str = "http://localhost:5173/oauth/callback?token="

    CELERY_WORKER_APP_NAME: str = ""
    CELERY_WORKER_BROKER: str = ""
    CELERY_WORKER_BACKEND: str = ""

    SENTRY_DSN: str = ""





settings = Settings()
