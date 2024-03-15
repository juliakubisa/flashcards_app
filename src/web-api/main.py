from flask import *
import os
from io import TextIOWrapper
from src.application.card import Card
from src.application.sql_database import db
from src.application.utils import allowed_file_extension
from src.application.input import read_input_file


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_CONNECTION_STRING']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # restrict max size to 16MB

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/cards")
def return_cards():
    all_cards = db.session.query(Card).all()
    return jsonify(all_cards)


@app.route("/card/<card_id>", methods = ['DELETE'])
def delete_card(card_id):
    card_to_delete = Card.query.get(card_id)
    db.session.delete(card_to_delete)
    db.session.commit()
    return "Card deleted", 200

@app.route("/card", methods= ['POST'])
def add_card():
    body = request.get_json()
    existing_card = (db.session.query(Card)
                     .filter_by(foreign_word=body['foreign_word']
                                , translated_word=body['translated_word']))
    if existing_card is None:
        new_card = Card(body['foreign_word'], body['translated_word'])
        db.session.add(new_card)
        db.session.commit()
        return "Card sucesfully added", 200
    else:
        return "This card already exists!", 409

@app.route("/card/<card_id>", methods=['PUT'])
def edit_card(card_id):
    body = request.get_json()
    card_to_edit = Card.query.get(card_id)
    card_to_edit.foreign_word = body['foreign_word']
    card_to_edit.translated_word = body['translated_word']
    db.session.commit()
    return "Card edited", 200

@app.route("/card/file", methods=['POST'])
def upload_cards_from_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No selected file', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file_extension(file.filename):
            csv_file = TextIOWrapper(file.stream, encoding='utf-8')
            cards_unknown_unique = read_input_file(csv_file)
            print([x for x in cards_unknown_unique])
            db.session.add_all(cards_unknown_unique)
            db.session.commit()
            return 'Cards added', 200