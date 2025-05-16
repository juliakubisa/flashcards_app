from src.application.model.input import CreateCardQuizLogRequest
from src.application.model.output import CreateCardQuizLogResponse
from src.domain.entities import CardQuizLog
from src.infrastructure.database.repositories import CardQuizLogRepository, DeckRepository, CardRepository
from src.domain.exceptions import NotExistsException


class CreateCardQuizLogCommand:
    def __init__(self, card_quiz_log_repository: CardQuizLogRepository,
                 deck_repository: DeckRepository,
                 card_repository: CardRepository):
        self.card_quiz_log_repository = card_quiz_log_repository
        self.deck_repository = deck_repository
        self.card_repository = card_repository

    def handle(self, deck_id: int, request: CreateCardQuizLogRequest, account_id: int) -> CreateCardQuizLogResponse:

        deck = self.deck_repository.get_by_id(deck_id)

        if deck is None or deck.account_id != account_id:
            raise NotExistsException("Deck not found")

        new_card_quiz_log = CardQuizLog(card_id=request.card_id, 
                        timestamp=request.timestamp, 
                        answer_correct = request.answer_correct,
                        response_time = request.response_time,
                        answer_type = request.answer_type)
        new_card_quiz_log_id = self.card_quiz_log_repository.add(new_card_quiz_log)


        card_to_update = self.card_repository.get_by_id(request.card_id)

        if card_to_update is None:
            raise NotExistsException("Card not found")

        card_to_update.total_quizzed = card_to_update.total_quizzed + 1
        card_to_update.total_correct_answers += 1 if request.answer_correct == 1 else 0
        card_to_update.timestamp_last_review = request.timestamp
        self.card_repository.save_changes(card_to_update)

        ### update p_recall 

        # new_p_recall = Algorithm.calculate_p_recall(card_to_update)
        # card_to_update.p_recall = new_p_recall
        
        return CreateCardQuizLogResponse(id=new_card_quiz_log_id)
    