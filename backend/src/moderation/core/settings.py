from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Content Moderation"
    ENVIRONMENT: str = "development"
    DB_URI: PostgresDsn

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
