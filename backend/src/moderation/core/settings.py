from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Content Moderation"
    ENVIRONMENT: str = "development"
    DB_URI: PostgresDsn

    # Kafka Configuration
    KAFKA_TOPIC: str = "moderation-content"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_GROUP_ID: str = "moderation-group"
    KAFKA_AUTO_OFFSET_RESET: str = "earliest"

    # Consumer Configuration
    MAX_RETRIES: int = 10
    RETRY_INTERVAL: int = 3
    CONSUMER_TIMEOUT_MS: int = 5000
    HEARTBEAT_INTERVAL: int = 60


settings = Settings()
