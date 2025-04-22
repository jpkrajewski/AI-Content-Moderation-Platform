from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Content Moderation"
    ENVIRONMENT: str = "development"
    DB_URI: str
    APP_HOST: str
    APP_PORT: int

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

    AI_IMAGE_MODERATION_MODEL: str = "Falconsai/nsfw_image_detection"
    AI_TEXT_MODERATION_MODEL: str = "unitary/toxic-bert"

    AI_IMAGE_MODERATION_THRESHOLD: float = 0.5
    AI_TEXT_MODERATION_THRESHOLD: float = 0.5


settings = Settings()
