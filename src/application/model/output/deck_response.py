from pydantic import BaseModel
from src.domain.entities.deck import Deck


class DeckResponse(BaseModel):
    id: int
    name: str
    language_name: str
    language_id: str
    cards_count: int

    def from_deck(deck: Deck):
        return DeckResponse(id=deck.id, 
                            name=deck.name, 
                            language_name=deck.language.name, 
                            language_id=deck.language_id, 
                            cards_count=len(deck.cards))
