from datetime import date
from flask import *
from io import StringIO
from sqlalchemy import exists, not_
from src.application.algorithm import Algorithm
from src.application.card import Card
from src.application.sql_database import db
from src.application.utils import allowed_file_extension
from src.application.input import read_input_file
from src.web_api.controllers.utils import edit_add_card_conditions

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
    does_card_exist = db.session.query(exists().where(Card.foreign_word == body['foreign_word'])
                                       .where(Card.translated_word == body['translated_word'])).scalar()

    condition, new_card = edit_add_card_conditions(body, does_card_exist, 'input')  # new card can be None or card
    if condition is True:
        db.session.add(new_card)
        db.session.commit()
        return "Card sucesfully added", 200
    else:
        # condition is used as an error message (str)
        return condition, 400 if new_card is None else 409


@card_controller.route("/card/<card_id>", methods=['PUT'])
def edit_card(card_id):
    body = request.get_json()
    does_card_exist = db.session.query(exists()
                                       .where(Card.foreign_word == body['foreign_word'])
                                       .where(Card.translated_word == body['translated_word'])
                                       .where(not_(Card.id == body['id']))).scalar()
    condition, edited_card = edit_add_card_conditions(body, does_card_exist, 'edit')
    if condition is True:
        card_to_edit = Card.query.get(card_id)
        card_to_edit.foreign_word = body['foreign_word']
        card_to_edit.translated_word = body['translated_word']
        db.session.commit()
        return "Card edited", 200
    else:
        return condition, 409


@card_controller.route("/card/file", methods=['POST'])
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


@card_controller.route("/cards/quiz", methods=['GET'])
def return_quiz_cards():
    all_cards = db.session.query(Card).all()
    algorithm = Algorithm(all_cards)
    algorithm.set_weights()
    cards_to_quiz = algorithm.select_quiz_cards()
    return jsonify(cards_to_quiz)


@card_controller.route("/cards/quiz", methods=['PUT'])
def update_card_statistics():
    body = request.get_json()
    date_now = date.today()
    
    ids_to_update = [card['id'] for card in body]
    cards_to_update = db.session.query(Card).filter(Card.id.in_(ids_to_update)).all()

    for card in cards_to_update:
        new_data = next((data for data in body if data["id"] == card.id), None)

        card.date_last_review = date_now
        card.answer_time = new_data['answer_time_ms']
        card.last_answer_correct = new_data['last_answer_correct']

        if new_data['last_answer_correct']:
            card.number_correct_answers = card.number_correct_answers + 1
        
    db.session.commit()
    return "Statistics updated", 200
