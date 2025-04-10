from typing import List
from src.domain.entities.entity_base import EntityBase
from src.domain.entities.language import Language
from src.domain.entities.card import Card
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Deck(EntityBase):
    __tablename__ = "deck"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))
    # Many to one: one deck can have only one language but language can have multiple decks
    language: Mapped["Language"] = relationship()
    # one to many when Deck is the parent class
    cards: Mapped[List["Card"]] = relationship(cascade="all, delete-orphan")

    def __init__(self, deck_name, language_id):
        self.name = deck_name
        self.language_id = language_id
