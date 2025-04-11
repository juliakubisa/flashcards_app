from src.application.model.output import CardResponse
from src.domain.exceptions import NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository


class GetCardsInDeckQuery:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository

    def handle(self, deck_id: int, account_id: int) -> list[CardResponse]:
        deck = self.deck_repository.get_by_id(deck_id)

        if deck is None or deck.account_id != account_id:
            raise NotExistsException('Deck not found')

        cards = self.card_repository.get_all_in_deck(deck_id)

        cards_response = [CardResponse.from_card(card) for card in cards]
        return cards_response