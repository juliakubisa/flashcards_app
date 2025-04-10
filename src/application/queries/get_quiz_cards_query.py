from src.application.algorithm import Algorithm
from src.application.model.output import QuizCardResponse
from src.infrastructure.database.repositories import CardRepository
from src.domain.exceptions.too_few_cards_exception import TooFewCardsException


class GetQuizCardsQuery:
    def __init__(self, repository: CardRepository):
        self.repository = repository

    def handle(self, deck_id: int, num_cards: int) -> list[QuizCardResponse]:
        all_cards = self.repository.get_all_in_deck(deck_id)

        if len(all_cards) < 10:
            raise TooFewCardsException('Too few cards to quiz')

        algorithm = Algorithm(all_cards, num_cards)
        quiz_cards = algorithm.select_quiz_cards() 

        return quiz_cards