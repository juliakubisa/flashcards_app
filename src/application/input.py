from src.model.card import Card
import toolz


def read_input_file(input_data, deck_id, delimiter):
    cards_unknown = []
    for line in input_data:
        if delimiter in line:
            try:
                word_pair = line.strip().split(delimiter)
                foreign_word = word_pair[0].replace('"', '').strip()
                translated_word = word_pair[1].replace('"', '').strip()
                card = Card(foreign_word=foreign_word, translated_word=translated_word, deck_id=deck_id)
                cards_unknown.append(card)
            except:
                print('Upload the file in the right format')

    # delete duplicate words and translations
    cards_unknown_unique = toolz.unique(cards_unknown, key=lambda x: x.foreign_word + x.translated_word)
    return cards_unknown_unique
