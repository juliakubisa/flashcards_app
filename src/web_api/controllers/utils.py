from src.application.card import Card
from src.application.utils import max_dict_value_len


def edit_add_card_conditions(body, does_card_exist, action_type):
    if 'foreign_word' not in body or 'translated_word' not in body:
        return "The fields cannot be empty", None

    max_foreign_len = max_dict_value_len(100, "foreign_word", body)
    max_transl_len = max_dict_value_len(100, "translated_word", body)

    if does_card_exist:
        return "This card already exists!", None
    elif not max_foreign_len or not max_transl_len:
        return "Input is too long", None
    elif not(body['foreign_word'] and body['translated_word']):
        return "The fields cannot be empty", None
    elif body['foreign_word'] and body['translated_word']:
        if action_type == 'input':
            new_card = Card(body['foreign_word'], body['translated_word'])
            return True, new_card
        else:
            return True, None
    else:
        return "The fields cannot be empty", None
