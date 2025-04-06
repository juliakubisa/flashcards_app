from sqlalchemy.orm import Session
from src.domain.entities.card import Card


class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_in_deck(self, id: int) -> list[Card]:
        return self.db.query(Card).filter(Card.deck_id == id).all()
    
