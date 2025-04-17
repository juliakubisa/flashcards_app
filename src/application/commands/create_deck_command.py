from src.application.model.input import CreateDeckRequest
from src.application.model.output import CreateDeckResponse
from src.domain.entities import Deck
from src.domain.exceptions import DuplicateException, FieldEmptyException
from src.infrastructure.database.repositories import DeckRepository

class CreateDeckCommand:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, request: CreateDeckRequest, account_id: int) -> CreateDeckResponse:
        if request.name is None:
            raise FieldEmptyException("Deck name is required")
        if request.language_id is None:
            raise FieldEmptyException("Deck language is required")

        duplicate_deck = self.repository.get_by_name(request.name)

        if duplicate_deck is not None and duplicate_deck.account_id == account_id:
            raise DuplicateException("Deck with such name already exists")
        
        new_deck = Deck(request.name, request.language_id, account_id)
        new_deck_id = self.repository.add(new_deck)
        return CreateDeckResponse(id=new_deck_id)