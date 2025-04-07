from src.application.model.output import DeckResponse
from src.infrastructure.database.repositories import DeckRepository

class GetDeckQuery:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, deck_id: int) -> DeckResponse | None:
        deck = self.repository.get_by_id(deck_id)

        if deck is None:
            return None

        deck_response = DeckResponse.from_deck(deck)
        return deck_response