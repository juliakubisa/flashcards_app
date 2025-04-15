from src.web_api.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


settings = Settings.load()

db_engine = create_engine(settings.database_connection_string, echo=False, pool_pre_ping=True)

LocalSession = sessionmaker(db_engine)