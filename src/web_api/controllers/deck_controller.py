from flask import *
from datetime import date
from io import StringIO
from sqlalchemy import exists
from sqlalchemy.orm import joinedload
from src.application.algorithm import Algorithm
from src.model.card import Card
from src.model.deck import Deck
from src.application.sql_database import db
from src.application.utils import allowed_file_extension
from src.application.input import read_input_file
from src.web_api.controllers.utils import add_card_conditions
from src.model.deck_dto import DeckDTO

deck_controller = Blueprint('deck_controller', __name__)


@deck_controller.route("/decks", methods=['GET'])
def return_decks():
    all_decks = db.session.query(Deck).all()
    decks_dtos = [DeckDTO(deck) for deck in all_decks]
    return jsonify([dto.__dict__ for dto in decks_dtos])


@deck_controller.route("/decks", methods=['POST'])
def add_deck():
    body = request.get_json()

    if not body['name']: 
        return 'Name cannot be empty', 400
    if not body['language_id']: 
        return 'Language cannot be empty', 400

    does_deck_exist = db.session.query(exists().where(Deck.name == body['name'])).scalar()
    
    new_deck = Deck(deck_name=body['name'], language_id=body['language_id'])

    if not does_deck_exist:
        db.session.add(new_deck)
        db.session.commit()
        return "Deck sucesfully added", 200
    else:
        return "Deck already exists", 409


@deck_controller.route("/decks/<deck_id>", methods=['DELETE'])
def delete_deck(deck_id):
    deck_to_delete = Deck.query.get(deck_id)

    if deck_to_delete is None: 
        return 'Deck does not exist', 404

    db.session.delete(deck_to_delete)
    db.session.commit()
    return 'Deck deleted', 200


@deck_controller.route("/decks/<deck_id>/cards", methods=['GET'])
def return_cards_in_deck(deck_id):
    deck = db.session.query(Deck).filter(Deck.id == deck_id).options(joinedload(Deck.cards)).first()
    return jsonify(deck.cards)


@deck_controller.route("/decks/<deck_id>/card", methods=['POST'])
def add_card(deck_id):
    body = request.get_json()
    does_card_exist = db.session.query(exists().where(Card.foreign_word == body['foreign_word'])
                                       .where(Card.translated_word == body['translated_word'])
                                       .where(Card.deck_id == body['deck_id'])).scalar()

    condition_output, new_card = add_card_conditions(body, does_card_exist, deck_id)
    if condition_output is True:
        db.session.add(new_card)
        db.session.commit()
        return "Card sucesfully added", 200
    else:
        # condition can return also an error message (str)
        return condition_output, 400 if new_card is None else 409


@deck_controller.route("/decks/<deck_id>/file", methods=['POST'])
def upload_cards_from_csv(deck_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No selected file', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if not allowed_file_extension(file.filename):
            return 'Unsupported file extension', 400
        if file and allowed_file_extension(file.filename):
            raw_data = StringIO(file.stream.read().decode("UTF8"), newline=None)
            delimiter = request.form['delimiter']
            cards_unknown_unique = read_input_file(raw_data, deck_id, delimiter)
            db.session.add_all(cards_unknown_unique)
            db.session.commit()
            return 'Cards added', 200


@deck_controller.route("/decks/<deck_id>/quiz/cards", methods=['GET'])
def return_quiz_cards(deck_id):
    all_cards = db.session.query(Deck).filter(Deck.id == deck_id).options(joinedload(Deck.cards)).first().cards
    algorithm = Algorithm(all_cards)
    algorithm.set_weights()
    cards_to_quiz = algorithm.select_quiz_cards()
    return jsonify([card.__dict__ for card in cards_to_quiz])


@deck_controller.route("/decks/<deck_id>/quiz/results", methods=['PUT'])
def update_card_statistics(deck_id):
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
