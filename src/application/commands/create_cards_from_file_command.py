from src.application.model.input import CreateCardRequest
from src.application.model.output import CreateCardResponse
from src.domain.entities import Card
from src.domain.exceptions import DuplicateException, FieldTooLongException, FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository

class CreateCardsFromFileCommand:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository

    def handle(self, deck_id: int, file_bytes: bytes) -> list[CreateCardResponse]:
        pass
