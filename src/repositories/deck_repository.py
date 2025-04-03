from sqlalchemy.orm import Session
from src.domain.deck import Deck

class DeckRepository:
    def __init__(self, db: Session):
        self.db = db
        pass

    def get_all(self):
        return self.db.query(Deck).all()