from src.application.model.input import CreateCardRequest
from src.domain.entities import Card
from src.domain.exceptions import DuplicateException, FieldTooLongException, FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository


class UpdateCardCommand:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository
        self.max_word_len = 100

    def handle(self, request: CreateCardRequest, card_id: int, account_id: int) -> None:

        if len(request.foreign_word) == 0:
            raise FieldEmptyException("Foreign word is required")

        if len(request.translated_word) == 0:
            raise FieldEmptyException("Translated word is required")
                
        if len(request.foreign_word) > self.max_word_len:
            raise FieldTooLongException("Foreign word too long")

        if len(request.translated_word) > self.max_word_len:
            raise FieldTooLongException("Translated word too long")
        
        existing_card = self.card_repository.get_by_id(card_id)

        if existing_card is None: 
            raise NotExistsException("Card not found")
        
        deck = self.deck_repository.get_by_id(existing_card.deck_id)

        if deck.account_id != account_id:
            raise NotExistsException("Card not found")

        existing_card.foreign_word = request.foreign_word
        existing_card.translated_word = request.translated_word
        existing_card.example_sentence = request.example_sentence
        self.card_repository.save_changes(existing_card)