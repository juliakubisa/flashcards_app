from dataclasses import dataclass
from typing import List


@dataclass
class QuizCardDTO:

    def __init__(self, card_id: int, foreign_word: str, translated_word: str, wrong_answers: List[str]):
        self.id = card_id
        self.foreign_word = foreign_word
        self.translated_word = translated_word
        self.wrong_answers = wrong_answers


