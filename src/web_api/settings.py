from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_connection_string: str
    google_client_id: str

    # JWT settings
    jwt_secret: str
    access_token_age_seconds: int = 10
    refresh_token_age_seconds: int = 60 * 60 * 24 * 30 # 30 days by default

    @lru_cache
    def load():
        return Settings()
    
