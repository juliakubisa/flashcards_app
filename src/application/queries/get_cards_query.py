from src.application.model.output.deck_response import CardResponse
from src.infrastructure.database.repositories.deck_repository import DeckRepository

class GetDeckQuery:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, deck_id: int) -> CardResponse | None:
        deck = self.repository.get_by_id(deck_id)

        if deck is None:
            return None

        card_response = CardResponse.from_deck(deck)
        return card_response