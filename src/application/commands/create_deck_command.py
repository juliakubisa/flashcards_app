from src.application.model.input.create_deck_request import CreateDeckRequest
from src.application.model.output.create_deck_response import CreateDeckResponse
from src.domain.entities.deck import Deck
from src.domain.exceptions.duplicate_exception import DuplicateException
from src.infrastructure.repositories.deck_repository import DeckRepository

class CreateDeckCommand:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, request: CreateDeckRequest) -> CreateDeckResponse:
        existing_deck = self.repository.get_by_name(request.name)

        if existing_deck is not None:
            raise DuplicateException("Deck with such name already exists")
        
        new_deck = Deck(deck_name=request.name, language_id=request.language_id)
        new_deck_id = self.repository.add(new_deck)
        return CreateDeckResponse(id=new_deck_id)