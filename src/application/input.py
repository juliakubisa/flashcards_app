from src.application.card import Card
import toolz
cards_unknown = []
import csv

def read_input_file(input_data):
    for line in input_data:
        if " - " in line:
            try:
                word_pair = line.strip().split("-")
                foreign_word = word_pair[0].replace('"', '')
                translated_word = word_pair[1].replace('"', '')
                card = Card(foreign_word, translated_word)
                cards_unknown.append(card)
            except:
                print('Upload the file in the right format')

    # delete duplicate words and translations
    cards_unknown_unique = toolz.unique(cards_unknown, key = lambda x: x.foreign_word + x.translated_word)
    return cards_unknown_unique

    # if __name__ == '__main__':
