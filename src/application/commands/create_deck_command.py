from src.application.model.input import CreateDeckRequest
from src.application.model.output import CreateDeckResponse
from src.domain.entities import Deck
from src.domain.exceptions import DuplicateException, FieldEmptyException
from src.infrastructure.database.repositories import DeckRepository

class CreateDeckCommand:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, request: CreateDeckRequest) -> CreateDeckResponse:
        if request.name is None:
            raise FieldEmptyException("Deck name is required")
        if request.language_id is None:
            raise FieldEmptyException("Deck language is required")

        existing_deck = self.repository.get_by_name(request.name)

        if existing_deck is not None:
            raise DuplicateException("Deck with such name already exists")
        
        new_deck = Deck(deck_name=request.name, language_id=request.language_id)
        new_deck_id = self.repository.add(new_deck)
        return CreateDeckResponse(id=new_deck_id)