import os
from src.application.card import Card
import toolz
cards_unknown = []
import csv

def read_input_file(input_data):
    try:
        reader = csv.DictReader(input_data)
        data = [row for row in reader]
        for row in data:
            foreign_word = row[0].strip().replace('"', '')
            translated_word = row[1].strip().replace('"', '')
            card = Card(foreign_word, translated_word)
            cards_unknown.append(card)
    except:
        print('Upload the file in the right format')

    # delete duplicate words and translations
    cards_unknown_unique = toolz.unique(cards_unknown, key = lambda x: x.foreign_word + x.translated_word)
    return cards_unknown_unique


# if __name__ == '__main__':
