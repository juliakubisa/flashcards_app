example = 'example_words.csv'
words_unknown = {}
words_learned = {}
words_to_review = {}

def read_input_file(input_data):
    try:
        with open(input_data, 'r') as f:
            lines = f.readlines()
            for line in lines[:10]:
                if "-" in line:
                    word_pair = line.strip().split('-')
                    foreign_word = word_pair[0]
                    translated_word = word_pair[1]
                    words_unknown[foreign_word] = translated_word
                else:
                    pass
    except:
        print('Upload the file in the right format')

def input_words():
    foreign_word = input('New word')
    translated_word = input('Translation')
    words_unknown[foreign_word] = translated_word


read_input_file(example)
input_words()
# if __name__ == '__main__':
