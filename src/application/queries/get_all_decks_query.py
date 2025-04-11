from src.application.model.output import DeckResponse
from src.infrastructure.database.repositories import DeckRepository

class GetAllDecksQuery:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, account_id: int) -> list[DeckResponse]:
        decks = self.repository.get_all_for_account(account_id)
        decks_response = [DeckResponse.from_deck(deck) for deck in decks]
        return decks_response