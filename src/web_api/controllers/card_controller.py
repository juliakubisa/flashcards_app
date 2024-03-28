from flask import *
from io import StringIO
from sqlalchemy import exists, not_
from src.application.card import Card
from src.application.sql_database import db
from src.application.utils import allowed_file_extension, max_dict_value_len
from src.application.input import read_input_file

card_controller = Blueprint('card_controller', __name__)


@card_controller.route("/cards", methods=['GET'])
def return_cards():
    all_cards = db.session.query(Card).all()
    return jsonify(all_cards)


@card_controller.route("/card/<card_id>", methods=['DELETE'])
def delete_card(card_id):
    card_to_delete = Card.query.get(card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    return "Card deleted", 200


@card_controller.route("/card", methods=['POST'])
def add_card():
    body = request.get_json()
    max_foreign_len = max_dict_value_len(100, "foreign_word", body)
    max_transl_len = max_dict_value_len(100, "translated_word", body)
    does_card_exist = db.session.query(exists().where(Card.foreign_word == body['foreign_word'])
                                       .where(Card.translated_word == body['translated_word'])).scalar()
    if (does_card_exist is False and body['foreign_word'] and body['translated_word']
            and max_foreign_len and max_transl_len):
        new_card = Card(body['foreign_word'], body['translated_word'])
        db.session.add(new_card)
        db.session.commit()
        return "Card sucesfully added", 200
    elif does_card_exist:
        return "This card already exists!", 409
    elif max_foreign_len is False and max_transl_len is False:
        return "Input is too long", 400
    elif max_transl_len is False and max_foreign_len:
        return "Translated Word is too long", 400
    elif max_foreign_len is False and max_transl_len:
        return "Foreign Word is too long", 400
    else:
        return "The fields cannot be empty", 400


@card_controller.route("/card/<card_id>", methods=['PUT']) # TODO: length validation
def edit_card(card_id):
    body = request.get_json()
    does_card_exist = db.session.query(exists()
                                       .where(Card.foreign_word == body['foreign_word'])
                                       .where(Card.translated_word == body['translated_word'])
                                       .where(not_(Card.id == body['id']))).scalar()
    if not does_card_exist:
        card_to_edit = Card.query.get(card_id)
        card_to_edit.foreign_word = body['foreign_word']
        card_to_edit.translated_word = body['translated_word']
        db.session.commit()
        return "Card edited", 200
    else:
        return "Card with these parameters already exists!", 409

@card_controller.route("/card/file", methods=['GET', 'POST'])
def upload_cards_from_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No selected file', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file_extension(file.filename):
            csv_data = StringIO(file.stream.read().decode("UTF8"), newline=None)
            cards_unknown_unique = read_input_file(csv_data)
            db.session.add_all(cards_unknown_unique)
            db.session.commit()
            return 'Cards added', 200