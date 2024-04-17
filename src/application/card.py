import binary

from src.application.sql_database import db
from sqlalchemy.orm import Mapped, mapped_column
from dataclasses import dataclass
from sqlalchemy import func, ForeignKey
from datetime import datetime
from typing import Optional

@dataclass
class Card(db.Model):
    # Basic Information
    id: Mapped[int] = mapped_column(primary_key= True)
    foreign_word: Mapped[str] = mapped_column()
    translated_word: Mapped[str] = mapped_column()
    #date_added: Mapped[datetime] = mapped_column(insert_default=func.now())
    #language: Mapped[str] = mapped_column(ForeignKey("language.id"))  #TODO: foreign_key vs relationship

    # Algorithm information
    easiness_factor: Mapped[float] = mapped_column(default=5)
    days_since_last_review: Mapped[int] = mapped_column()
    last_answer_correct: Mapped[bool] = mapped_column()
    number_correct_answers: Mapped[float] = mapped_column()
    answer_time: Mapped[float] = mapped_column()

    # Probability of being drawn
    #probability: Mapped[float] = mapped_column()

    def __init__(self, foreign_word, translated_word):
        self.foreign_word = foreign_word
        self.translated_word = translated_word
        self.easiness_factor = 5
        self.days_since_last_review = 0
        self.last_answer_correct = False
        self.number_correct_answers = 0
        self.answer_time = 0
