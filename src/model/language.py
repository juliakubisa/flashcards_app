from src.application.sql_database import db
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship

@dataclass
class Language(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __init__(self, lang_name, lang_code):
        self.id = lang_code
        self.name = lang_name
