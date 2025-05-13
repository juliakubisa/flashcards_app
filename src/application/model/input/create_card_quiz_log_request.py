from pydantic import BaseModel
import datetime


class CreateCardQuizLogRequest(BaseModel):
    timestamp: datetime.datetime
    answer_correct: bool
    response_time: int
    answer_type: int
    card_id: int
