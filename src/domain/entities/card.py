from src.domain.entities.entity_base import EntityBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from datetime import date


class Card(EntityBase):
    __tablename__ = "card"

    # Basic Information
    id: Mapped[int] = mapped_column(primary_key= True)
    foreign_word: Mapped[str] = mapped_column()
    translated_word: Mapped[str] = mapped_column()
    date_added: Mapped[date] = mapped_column(insert_default=func.now())
    deck_id: Mapped[int] = mapped_column(ForeignKey("deck.id"))
    example_sentence: Mapped[str] = mapped_column(default=None, nullable=True)

    # Algorithm information
    easiness_factor: Mapped[float] = mapped_column(default=1)
    last_answer_correct: Mapped[bool] = mapped_column(default=False)
    number_correct_answers: Mapped[float] = mapped_column(default=0)
    answer_time: Mapped[float] = mapped_column(default=0)
    date_last_review: Mapped[date] = mapped_column(default=None, nullable=True)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
