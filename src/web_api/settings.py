from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database settings
    database_connection_string: str

    # External login providers settings
    google_client_id: str

    # Application web domain e.g. .flashcards.com
    domain: str | None = None

    # JWT settings
    jwt_secret: str
    access_token_age_seconds: int = 10 * 60 # 10 minutes by default
    refresh_token_age_seconds: int = 60 * 60 * 24 * 30 # 30 days by default

    # AWS settings
    aws_access_key_id: str
    aws_secret_access_key: str

    @lru_cache
    def load():
        return Settings()
    
