from src.application.sql_database import db
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column

@dataclass
class Language(db.Model):
    # __tablename__ = "language"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[float] = mapped_column()

    def __init__(self, language_name):
        self.name = language_name
