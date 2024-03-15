from src.application.sql_database import db
from sqlalchemy.orm import Mapped, mapped_column
from dataclasses import dataclass


@dataclass
class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key= True)
    foreign_word: Mapped[str] = mapped_column()
    translated_word: Mapped[str] = mapped_column()

    def __init__(self, foreign_word, translated_word):
        self.foreign_word = foreign_word
        self.translated_word = translated_word