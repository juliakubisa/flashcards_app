from src.application.sql_database import db
from src.application.language import Language
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

@dataclass
class Language(db.Model):
    # __tablename__ = "deck"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[float] = mapped_column()
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))
    # Many to one: one deck can have only one language but language can have multiple decks
    language: Mapped["Language"] = relationship()

    def __init__(self, deck_name):
        self.name = deck_name
