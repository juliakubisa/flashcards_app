from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_connection_string: str
    google_client_id: str
    domain: str | None = None

    # JWT settings
    jwt_secret: str
    access_token_age_seconds: int = 10 * 60 # 10 minutes by default
    refresh_token_age_seconds: int = 60 * 60 * 24 * 30 # 30 days by default

    @lru_cache
    def load():
        return Settings()
    
