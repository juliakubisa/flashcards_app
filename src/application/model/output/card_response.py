from datetime import date
from pydantic import BaseModel
from src.domain.entities.card import Card

class CardResponse(BaseModel):
    id: int
    foreign_word: str
    translated_word: str
    date_added: date
    example_sentence: str 

    def from_card(card: Card):
        return CardResponse(id=card.id, 
                            foreign_word= card.foreign_word,
                            translated_word= card.translated_word,
                            date_added=card.date_added,
                            example_sentence = card.example_sentence)
    