from src.domain.exceptions import NotExistsException
from src.infrastructure.database.repositories import CardRepository

class DeleteCardCommand:
    def __init__(self, repository: CardRepository):
        self.repository = repository

    def handle(self, card_id: int) -> None:
        card = self.repository.get_by_id(card_id)

        if card is None:
            raise NotExistsException("Card not found")
        
        self.repository.delete(card)