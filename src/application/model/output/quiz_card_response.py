from pydantic import BaseModel


class QuizCardResponse(BaseModel):
    id: int
    foreign_word: str
    translated_word: str
    wrong_answers: list[str]
