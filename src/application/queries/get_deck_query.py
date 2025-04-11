from src.application.model.output import DeckResponse
from src.domain.exceptions.not_exists_exception import NotExistsException
from src.infrastructure.database.repositories import DeckRepository
from src.domain.exceptions import FieldEmptyException

class GetDeckQuery:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, deck_id: int, account_id: int) -> DeckResponse | None:
        if deck_id is None:
            raise FieldEmptyException("Deck ID is required")

        deck = self.repository.get_by_id(deck_id)

        if deck is None or deck.account_id != account_id:
            raise NotExistsException("Deck not found")

        deck_response = DeckResponse.from_deck(deck)
        return deck_response