from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_connection_string: str
    
    # TODO: to be added during refactoring
    # jwt_secret: str
    # google_client_id: str

    @lru_cache
    def load():
        return Settings()
    
