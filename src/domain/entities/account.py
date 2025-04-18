from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .deck import Deck
from .entity_base import EntityBase


class Account(EntityBase):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    google_id: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    refresh_token: Mapped[str] = mapped_column(nullable=True)
    decks: Mapped[List["Deck"]] = relationship()

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
