from enum import Enum


class SortDecksBy(str, Enum):
    NAME = 'name'
    LANGUAGE = 'language_id'
    NUMBER_OF_CARDS = 'number_of_cards'
    DATE_OF_LAST_QUIZ = 'date_of_last_quiz'