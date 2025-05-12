from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session
from src.domain.entities import Deck, Card
from src.domain.enums import SortDecksBy, SortDirection

class DeckRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_account(self, account_id: int, sort_by: SortDecksBy, sort_direction: SortDirection) -> list[Deck]:
        return (self.db.query(Deck)
                .join(Card, Deck.id == Card.deck_id)
                .group_by(Deck.id)
                .filter(Deck.account_id == account_id)
                .order_by(self.__get_sort_expression(sort_by, sort_direction))
                .all())
    
    def get_by_id(self, id: int) -> Deck | None:
        return (self.db.query(Deck)
                .filter(Deck.id == id)
                .one_or_none())
    
    def get_by_name(self, name: str) -> Deck | None:
        return (self.db.query(Deck)
                .filter(Deck.name == name)
                .one_or_none())
    
    def add(self, deck: Deck) -> int:
        self.db.add(deck)
        self.db.commit()
        self.db.refresh(deck)
        return deck.id
    
    def delete(self, deck: Deck) -> None:
        self.db.delete(deck)
        self.db.commit()

    def save_changes(self, deck: Deck) -> None:
        self.db.commit()
        self.db.refresh(deck) 

    def __get_sort_expression(self, sort_by: SortDecksBy, sort_direction: SortDirection):

        if sort_by == SortDecksBy.NUMBER_OF_CARDS:
            sort_column = func.count(Card.id)
        else:
            sort_column = getattr(Deck, sort_by.value)

        if sort_direction == SortDirection.DESCENDING:
            sort = desc(sort_column)
        else:
            sort = asc(sort_column)

        return sort
