from typing import List
from src.application.sql_database import db
from src.model.language import Language
from src.model.card import Card
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


@dataclass
class Deck(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"))
    # Many to one: one deck can have only one language but language can have multiple decks
    language: Mapped["Language"] = relationship()
    # one to many when Deck is the parent class
    cards: Mapped[List["Card"]] = relationship(cascade="all, delete-orphan")

    def __init__(self, deck_name, language_id):
        self.name = deck_name
        self.language_id = language_id
