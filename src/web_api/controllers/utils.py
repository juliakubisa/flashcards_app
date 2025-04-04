from src.domain.entities.card import Card
from src.application.utils import max_dict_value_len


def edit_add_card_conditions(does_card_exist, body, card):
    if 'foreign_word' not in body or 'translated_word' not in body:
        return "The fields cannot be empty", None

    max_foreign_len = max_dict_value_len(100, "foreign_word", body)
    max_transl_len = max_dict_value_len(100, "translated_word", body)

    if does_card_exist:
        return "This card already exists!", None
    elif not max_foreign_len or not max_transl_len:
        return "Input is too long", None
    elif not (body['foreign_word'] and body['translated_word']):
        return "The fields cannot be empty", None
    elif body['foreign_word'] and body['translated_word']:
        return True, card
    else:
        return "The fields cannot be empty", None


def add_card_conditions(does_card_exist, body, deck_id):
    return edit_add_card_conditions(does_card_exist, body,
                                    Card(foreign_word=body['foreign_word'],
                                         translated_word=body['translated_word'],
                                         deck_id=deck_id))


def edit_card_conditions(body, does_card_exist):
    return edit_add_card_conditions(does_card_exist, body,
                                    Card(foreign_word=body['foreign_word'],
                                         translated_word=body['translated_word']))
