class Card:
    is_known = False

    def __init__(self, foreign_word, translated_word):
        self.foreign_word = foreign_word
        self.translated_word = translated_word

    def set_as_known(self):
        self.is_known = True
