from src.domain.exceptions.not_exists_exception import NotExistsException
from src.infrastructure.database.repositories.deck_repository import DeckRepository

class DeleteDeckCommand:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, deck_id: int) -> None:
        deck = self.repository.get_by_id(deck_id)

        if deck is None:
            raise NotExistsException("Deck not found")
        
        self.repository.delete(deck)