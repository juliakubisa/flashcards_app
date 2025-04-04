from sqlalchemy.orm import Session
from src.domain.entities.language import Language

class LanguageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Language]:
        return self.db.query(Language).all()
