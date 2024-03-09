import os
from src.application.card import Card
import toolz
cards_unknown = []


def read_input_file(input_data):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, input_data)

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines[:10]: # change to ':'
                if "-" in line:
                    word_pair = line.strip().split('-')
                    foreign_word = word_pair[0]
                    translated_word = word_pair[1]
                    card = Card(foreign_word, translated_word)
                    cards_unknown.append(card)
                else:
                    pass
    except:
        print('Upload the file in the right format')

    # delete duplicate objects
    cards_unknown_unique = toolz.unique(cards_unknown, key = lambda x: x.foreign_word + x.translated_word)
    return cards_unknown_unique

# read_input_file('example_words.csv')
# if __name__ == '__main__':
