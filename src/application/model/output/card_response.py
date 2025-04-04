from pydantic import BaseModel
from src.domain.entities.card import Card

class CardResponse(BaseModel):
    id: int
    foreign_word: str
    translated_word: str
    date_added: int
    deck_id: int

    def from_deck(card: Card):
        return CardResponse(id=card.id, 
                            foreign_word= card.foreign_word,
                            translated_word= card.translated_word,
                            date_added=card.date_added,
                            deck_id = card.deck_id)
    