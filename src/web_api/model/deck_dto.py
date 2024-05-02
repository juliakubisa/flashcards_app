from dataclasses import dataclass


@dataclass
class DeckDTO:
    def __init__(self, deck):
        self.id = deck.id
        self.name = deck.name
        self.language = deck.language_id
        self.cards_count = len(deck.cards)