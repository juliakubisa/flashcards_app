from sqlalchemy.orm import Session
from src.domain.deck import Deck

class DeckRepository:
    def __init__(self, db: Session):
        self.db = db
        pass

    def get_all(self) -> list[Deck]:
        return self.db.query(Deck).all()
    
    def get_by_id(self, id: int) -> Deck | None:
        return self.db.query(Deck).filter(Deck.id == id).one_or_none()
