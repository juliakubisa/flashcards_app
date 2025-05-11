from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from src.domain.entities.card import Card


class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_all_in_deck(self, deck_id: int) -> int:
        return self.db.query(Card).filter(Card.deck_id == deck_id).count()
    
    def count_specific_in_deck(self, deck_id: int, search_text: str) -> int:
        return self.db.query(Card).filter(and_(Card.deck_id == deck_id, or_(Card.foreign_word.ilike(f"%{search_text}%"), Card.translated_word.ilike(f"%{search_text}%")))).count()

    def get_several_in_deck(self, deck_id: int, offset: int, limit: int) -> list[Card]:
        return self.db.query(Card).filter(Card.deck_id == deck_id).order_by(Card.date_added.desc()).offset(offset).limit(limit).all()
    
    def get_specific_in_deck(self, deck_id: int, offset: int, limit: int, search_text: str) -> list[Card]:
        return self.db.query(Card).filter(and_(Card.deck_id == deck_id, or_(Card.foreign_word.ilike(f"%{search_text}%"), Card.translated_word.ilike(f"%{search_text}%")))).order_by(Card.date_added.desc()).offset(offset).limit(limit).all()
    
    def get_all_in_deck(self, deck_id: int) -> list[Card]:
        return self.db.query(Card).filter(Card.deck_id == deck_id).order_by(Card.date_added.desc()).all()

    def get_by_id(self, id: int) -> Card | None:
        return self.db.query(Card).filter(Card.id == id).one_or_none()
    
    def get_in_deck(self, id: int, foreign_word: str, translated_word: str) -> Card | None:
        return self.db.query(Card).filter(Card.deck_id==id, Card.foreign_word==foreign_word, Card.translated_word==translated_word).one_or_none()
    
    def add(self, card: Card) -> int:
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card.id
    
    def add_many(self, cards: list[Card]) -> list[int]:
        self.db.add_all(cards)
        self.db.commit()

        for card in cards:
            self.db.refresh(card)

        return [c.id for c in cards]

    def delete(self, card: Card) -> None:
        self.db.delete(card)
        self.db.commit()

    def save_changes(self, card: Card) -> None:
        self.db.commit()
        self.db.refresh(card) 
