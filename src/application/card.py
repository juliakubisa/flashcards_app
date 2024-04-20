from src.application.sql_database import db
from sqlalchemy.orm import Mapped, mapped_column
from dataclasses import dataclass
from sqlalchemy import func, ForeignKey
from datetime import datetime


@dataclass
class Card(db.Model):
    # Basic Information
    id: Mapped[int] = mapped_column(primary_key= True)
    foreign_word: Mapped[str] = mapped_column()
    translated_word: Mapped[str] = mapped_column()
    # date_added: Mapped[datetime] = mapped_column(insert_default=func.now())
    # language: Mapped[str] = mapped_column(ForeignKey("language.id"))  #TODO: foreign_key vs relationship

    # Algorithm information
    easiness_factor: Mapped[float] = mapped_column(default=5)
    days_since_last_review: Mapped[int] = mapped_column(default=0)
    last_answer_correct: Mapped[bool] = mapped_column(default=False)
    number_correct_answers: Mapped[float] = mapped_column(default=0)
    answer_time: Mapped[float] = mapped_column(default=0)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
