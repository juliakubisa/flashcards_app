from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    foreign_word: str
    translated_word: str
    example_sentence: str