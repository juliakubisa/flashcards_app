from src.domain.exceptions.not_exists_exception import NotExistsException
from src.infrastructure.database.repositories.card_repository import CardRepository

class DeleteCardCommand:
    def __init__(self, repository: CardRepository):
        self.repository = repository

    def handle(self, card_id: int) -> None:
        card = self.repository.get_by_id(card_id)

        if card is None:
            raise NotExistsException("Card not found")
        
        self.repository.delete(card)