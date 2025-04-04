from sqlalchemy.orm import Session
from src.domain.entities.deck import Deck

class DeckRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Deck]:
        return self.db.query(Deck).all()
    
    def get_by_id(self, id: int) -> Deck | None:
        return self.db.query(Deck).filter(Deck.id == id).one_or_none()
    
    def get_by_name(self, name: str) -> Deck | None:
        return self.db.query(Deck).filter(Deck.name == name).one_or_none()
    
    def add(self, deck: Deck) -> int:
        self.db.add(deck)
        self.db.commit()
        self.db.refresh(deck)
        return deck.id
