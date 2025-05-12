from src.application.model.output import CardsPaginatedResponse, CardResponse
from src.domain.enums import SortCardsBy, SortDirection
from src.domain.exceptions import NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository


class GetCardsInDeckQuery:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository

    def handle(self, deck_id: int, account_id: int, page: int, page_size: int, search_text: str | None, sort_by: SortCardsBy, sort_direction: SortDirection) -> CardsPaginatedResponse:
        deck = self.deck_repository.get_by_id(deck_id)

        if deck is None or deck.account_id != account_id:
            raise NotExistsException('Deck not found')
        
        if search_text:
            cards = self.card_repository.get_specific_in_deck(deck_id, offset=page*page_size, limit=page_size, search_text=search_text, sort_by=sort_by, sort_direction=sort_direction)
            total_cards_count = self.card_repository.count_specific_in_deck(deck_id, search_text)
        else:
            cards = self.card_repository.get_several_in_deck(deck_id, offset=page*page_size, limit=page_size, sort_by=sort_by, sort_direction=sort_direction)
            total_cards_count = self.card_repository.count_all_in_deck(deck_id)

        cards_response = [CardResponse.from_card(card) for card in cards]

        paginated_response = CardsPaginatedResponse(items=cards_response, page=page, page_size=page_size, total=total_cards_count)

        return paginated_response