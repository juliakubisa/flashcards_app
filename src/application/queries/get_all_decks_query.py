from src.application.model.output import DeckResponse
from src.domain.enums import SortDecksBy, SortDirection
from src.infrastructure.database.repositories import DeckRepository

class GetAllDecksQuery:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, account_id: int, search_text: str | None, sort_by: SortDecksBy, sort_direction: SortDirection) -> list[DeckResponse]:
        if search_text:
            decks = self.repository.get_specific_for_account(account_id, search_text, sort_by, sort_direction)
        else:
            decks = self.repository.get_all_for_account(account_id, sort_by, sort_direction)
            
        decks_response = [DeckResponse.from_deck(deck) for deck in decks]
        return decks_response