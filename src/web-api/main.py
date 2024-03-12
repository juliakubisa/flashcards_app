from flask import *
from src.application.card import Card
from src.application.sql_database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
db.init_app(app)


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
    new_card = Card(body['foreign_word'], body['translated_word'])
    db.session.add(new_card)
    db.session.commit()
    return "Card sucesfully added", 200

@app.route("/card/<card_id>", methods=['PUT'])
def edit_card(card_id):
    body = request.get_json()
    card_to_edit = Card.query.get(card_id)
    card_to_edit.foreign_word = body['foreign_word']
    card_to_edit.translated_word = body['translated_word']
    db.session.commit()
    return "Card edited", 200
