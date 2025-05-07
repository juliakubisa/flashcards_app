import random
from difflib import get_close_matches
from src.application.model.output import QuizCardResponse
from src.domain.entities import Card


class Algorithm:

    def __init__(self, all_cards: list[Card], num_cards: int):
        self.all_cards = all_cards
        self.num_cards = num_cards
        # self.df = pd.DataFrame([c.__dict__ for c in all_cards])  # Convert Card objects to pandas dataframe

    def select_cards(self) -> list[Card]:
        cards = random.sample(self.all_cards, self.num_cards)
        return cards 
    
    def select_quiz_cards(self) -> list[QuizCardResponse]:
        cards = self.select_cards()
        quiz_cards = [QuizCardResponse(id=card.id, foreign_word=card.foreign_word, translated_word=card.translated_word, 
                                       wrong_answers=self.select_wrong_answers(card)) for card in cards]
        return quiz_cards

    def select_wrong_answers(self, card: Card) -> list:
        """Selects 3 other options for quiz ABCD mode"""
        candidates = [other_card.foreign_word for other_card in self.all_cards if other_card.foreign_word != card.foreign_word]
        wrong_answers = get_close_matches(card.foreign_word, candidates, 3)

        while len(wrong_answers) < 3:
            new_candidates = [word for word in candidates if candidates not in wrong_answers]
            sample = random.sample(new_candidates, 3-len(wrong_answers))
            wrong_answers.extend(sample)
        return wrong_answers
