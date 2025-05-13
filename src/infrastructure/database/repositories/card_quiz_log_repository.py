from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from src.domain.entities.card_quiz_log import CardQuizLog


class CardQuizLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, card_quiz_log: CardQuizLog) -> int:
        self.db.add(card_quiz_log)
        self.db.commit()
        self.db.refresh(card_quiz_log)
        return card_quiz_log.id