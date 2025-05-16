from src.application.algorithm import Algorithm
from src.application.model.output import QuizCardResponse
from src.infrastructure.database.repositories import CardRepository, DeckRepository
from src.domain.exceptions import TooFewCardsException, NotExistsException


class GetQuizCardsQuery:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository

    def handle(self, deck_id: int, num_cards: int, account_id: int) -> list[QuizCardResponse]:
        deck = self.deck_repository.get_by_id(deck_id)

        if deck is None or deck.account_id != account_id:
            raise NotExistsException("Deck not found")

        all_cards = self.card_repository.get_all_in_deck(deck_id)

        if len(all_cards) < 10:
            raise TooFewCardsException('Too few cards to quiz')

        algorithm = Algorithm()
        quiz_cards = algorithm.select_quiz_cards(all_cards, num_cards) 

        return quiz_cards