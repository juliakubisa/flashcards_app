from src.domain.entities.entity_base import EntityBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, ForeignKey
from datetime import date


class CardQuizLog(EntityBase):
    __tablename__ = "card_quiz_log"

    id: Mapped[int] = mapped_column(primary_key= True)
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"))
    timestamp: Mapped[date] = mapped_column(default=False)
    answer_correct: Mapped[bool] = mapped_column(default=False)
    response_time: Mapped[float] = mapped_column(default=False)
    answer_type: Mapped[int] = mapped_column(default=False)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
