from src.application.model.output.deck_response import DeckResponse
from src.repositories.deck_repository import DeckRepository

class GetAllDecks:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self):
        decks = self.repository.get_all()
        decks_response = [DeckResponse.from_deck(deck) for deck in decks]
        return decks_response