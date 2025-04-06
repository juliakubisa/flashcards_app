from src.application.model.input.create_card_request import CreateCardRequest
from src.application.model.output.create_card_response import CreateCardResponse
from src.domain.entities.card import Card
from src.domain.exceptions.duplicate_exception import DuplicateException
from src.domain.exceptions.field_too_long_exception import FieldTooLongException
from src.domain.exceptions.field_empty_exception import FieldEmptyException
from src.domain.exceptions.not_exists_exception import NotExistsException
from src.infrastructure.database.repositories.card_repository import CardRepository
from src.infrastructure.database.repositories.deck_repository import DeckRepository

class CreateCardCommand:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository
        self.max_word_len = 100

    def handle(self, deck_id: int, request: CreateCardRequest) -> CreateCardResponse:

        if len(request.foreign_word) == 0:
            raise FieldEmptyException("Foreign word is required")

        if len(request.translated_word) == 0:
            raise FieldEmptyException("Translated word is required")
                
        if len(request.foreign_word) > self.max_word_len:
            raise FieldTooLongException("Foreign word too long")

        if len(request.translated_word) > self.max_word_len:
            raise FieldTooLongException("Translated word too long")
        
        existing_deck = self.deck_repository.get_by_id(deck_id)

        if existing_deck is None: 
            raise NotExistsException("Deck not found")
        
        existing_card = self.card_repository.get_in_deck(deck_id, request.foreign_word, request.translated_word)

        if existing_card is not None:
            raise DuplicateException("Card already exists")
        
        new_card = Card(foreign_word=request.foreign_word, translated_word=request.translated_word, deck_id = deck_id)
        new_card_id = self.card_repository.add(new_card)
        return CreateCardResponse(id=new_card_id)
    

