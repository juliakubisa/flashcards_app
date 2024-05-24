import csv

from src.model.deck import Deck
from src.model.language import Language

csv_lines = []


def allowed_file_extension(filename):
    allowed_extensions = {'csv', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def clean_csv(csv_file):
    with open(csv_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if " - " in line:
                line_to_write = [line.strip().replace("'", '')]
                csv_lines.append(line_to_write)
            else:
                pass
    return csv_lines


def write_csv(data):
    with open('premade_data/example_csv2.csv', 'w') as f:
        csvwriter = csv.writer(f, delimiter="-")
        csvwriter.writerows(data)


def max_dict_value_len(length, key, d):
    value = d[key]
    max_length = len(value)
    return max_length <= length


def create_default_deck(db_session):
    decks = []
    decks_data = [
        {"name": "Test1"},
        {"name": "Test2"},
        {"name": "Test3"}
    ]

    for i, deck_data in enumerate(decks_data):
        deck = Deck(deck_name=deck_data['name'])
        english = db_session.query(Language).filter(Language.id == 'en').first()
        deck.language_id = english.id
        decks.append(deck)
    db_session.add_all(decks)
    db_session.commit()
