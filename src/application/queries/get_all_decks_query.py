from src.application.model.output.deck_response import DeckResponse
from src.infrastructure.database.repositories.deck_repository import DeckRepository

class GetAllDecksQuery:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self) -> list[DeckResponse]:
        decks = self.repository.get_all()
        decks_response = [DeckResponse.from_deck(deck) for deck in decks]
        return decks_response