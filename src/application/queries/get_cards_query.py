from src.application.model.output.card_response import CardResponse
from src.infrastructure.database.repositories.card_repository import CardRepository


class GetCardsInDeckQuery:
    def __init__(self, repository: CardRepository):
        self.repository = repository

    def handle(self, deck_id: int) -> list[CardResponse]:
        cards = self.repository.get_in_deck(deck_id)

        cards_response = [CardResponse.from_card(card) for card in cards]
        return cards_response