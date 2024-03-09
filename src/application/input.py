import os
from src.application.card import Card
example = 'example_words.csv'

# words_unknown = {}
# words_learned = {}
# words_to_review = {}
words_unknown = []


def read_input_file(input_data):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, input_data)

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines[:10]: # zmienić na dwukropek
                if "-" in line:
                    word_pair = line.strip().split('-')
                    foreign_word = word_pair[0]
                    translated_word = word_pair[1]
                    card = Card(foreign_word, translated_word)
                    words_unknown.append(card)
                else:
                    pass
    except:
        print('Upload the file in the right format')
    return words_unknown



read_input_file(example)
# input_words()
# if __name__ == '__main__':
