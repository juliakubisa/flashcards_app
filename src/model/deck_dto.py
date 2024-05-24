from dataclasses import dataclass


@dataclass
class DeckDTO:
    def __init__(self, deck):
        self.id = deck.id
        self.name = deck.name
        self.language_name = deck.language.name
        self.language_id = deck.language_id
        self.cards_count = len(deck.cards)