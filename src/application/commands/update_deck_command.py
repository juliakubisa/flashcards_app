from src.application.model.input import CreateDeckRequest
from src.domain.exceptions import DuplicateException, FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import DeckRepository


class UpdateDeckCommand:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def handle(self, request: CreateDeckRequest, deck_id: int, account_id: int) -> None:

        if not request.name:
            raise FieldEmptyException("Deck name is required")
        
        if not request.language_id:
            raise FieldEmptyException("Deck language is required") 

        existing_deck = self.repository.get_by_id(deck_id)

        if existing_deck is None or existing_deck.account_id != account_id: 
            raise NotExistsException("Deck not found")
        
        duplicate_deck = self.repository.get_by_name(request.name)

        if duplicate_deck is not None and duplicate_deck.account_id == account_id:
            raise DuplicateException("Deck with such name already exists")

        existing_deck.name = request.name
        existing_deck.language_id = request.language_id
        self.repository.save_changes(existing_deck)