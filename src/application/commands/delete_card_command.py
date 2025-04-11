from src.domain.exceptions import NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository

class DeleteCardCommand:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository

    def handle(self, card_id: int, account_id: int) -> None:
        card = self.card_repository.get_by_id(card_id)

        if card is None:
            raise NotExistsException("Card not found")

        deck = self.deck_repository.get_by_id(card.deck_id)

        if deck.account_id != account_id:
            raise NotExistsException("Card not found")
        
        self.card_repository.delete(card)