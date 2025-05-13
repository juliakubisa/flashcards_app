from src.application.model.input import CreateCardQuizLogRequest
from src.application.model.output import CreateCardQuizLogResponse
from src.domain.entities import CardQuizLog
from src.infrastructure.database.repositories import CardQuizLogRepository

class CreateCardQuizLogCommand:
    def __init__(self, card_quiz_log_repository: CardQuizLogRepository):
        self.card_quiz_log_repository = card_quiz_log_repository

    def handle(self, request: CreateCardQuizLogRequest, account_id: int) -> CreateCardQuizLogResponse:

        # czy cardy naleza do konkretnego konta
        # 

        new_card_quiz_log = CardQuizLog(card_id=request.card_id, 
                        timestamp=request.timestamp, 
                        answer_correct = request.answer_correct,
                        response_time = request.response_time,
                        answer_type = request.answer_type)
        new_card_quiz_log_id = self.card_quiz_log_repository.add(new_card_quiz_log)
        return CreateCardQuizLogResponse(id=new_card_quiz_log_id)
    
# Card -> kolumna included_in_last_quiz
# getQuizCards -> zaktualizuj ta kolumne
# quizResults -> sprawdz czy kazda wyslana carda jest oznaczona jako included_in_last_quiz