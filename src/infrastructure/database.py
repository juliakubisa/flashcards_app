from src.web_api.settings import Settings
from sqlalchemy import create_engine

settings = Settings.load()

db = create_engine(settings.database_connection_string, echo=True)