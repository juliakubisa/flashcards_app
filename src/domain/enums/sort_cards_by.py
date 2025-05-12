from enum import Enum


class SortCardsBy(str, Enum):
    FOREIGN_WORD = 'foreign_word'
    TRANSLATED_WORD = 'translated_word'
    DATE_ADDED = 'date_added'
    DATE_OF_LAST_QUIZ = 'date_of_last_quiz'