from src.application.model.input import CreateCardRequest
from src.application.model.output import CreateCardResponse
from src.domain.entities import Card
from src.domain.exceptions import DuplicateException, FieldTooLongException, FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository

class CreateCardCommand:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository
        self.max_word_len = 100

    def handle(self, deck_id: int, request: CreateCardRequest, account_id: int) -> CreateCardResponse:

        if len(request.foreign_word) == 0:
            raise FieldEmptyException("Foreign word is required")

        if len(request.translated_word) == 0:
            raise FieldEmptyException("Translated word is required")
                
        if len(request.foreign_word) > self.max_word_len:
            raise FieldTooLongException("Foreign word too long")

        if len(request.translated_word) > self.max_word_len:
            raise FieldTooLongException("Translated word too long")
        
        existing_deck = self.deck_repository.get_by_id(deck_id)

        if existing_deck is None or existing_deck.account_id != account_id: 
            raise NotExistsException("Deck not found")
        
        existing_card = self.card_repository.get_in_deck(deck_id, request.foreign_word, request.translated_word)

        if existing_card is not None:
            raise DuplicateException("Card already exists")
        
        new_card = Card(foreign_word=request.foreign_word, translated_word=request.translated_word, deck_id = deck_id)
        new_card_id = self.card_repository.add(new_card)
        return CreateCardResponse(id=new_card_id)
    

