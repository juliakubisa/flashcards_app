import os
from src.application.card import Card
import toolz
cards_unknown = []
import csv


def read_input_file(input_data):
    try:
        with open(input_data, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if " - " in line:
                    word_pair = line.strip().split('-')
                    foreign_word = word_pair[0].strip().replace('"', '')
                    translated_word = word_pair[1].strip().replace('"', '')
                    print(word_pair)
                    print(translated_word)
                    card = Card(foreign_word, translated_word)
                    cards_unknown.append(card)
                else:
                    pass
    except:
        print('Upload the file in the right format')

    # delete duplicate words and translations
    cards_unknown_unique = toolz.unique(cards_unknown, key = lambda x: x.foreign_word + x.translated_word)
    return cards_unknown_unique


# cards_unknown_unique = read_input_file('example_csv2.csv')
# print([x for x in cards_unknown_unique])
# if __name__ == '__main__':
