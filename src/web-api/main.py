from flask import Flask, jsonify
from src.application.card import Card
from src.application.sql_database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
db.init_app(app)


@app.route("/cards")
def return_cards():
    all_cards = db.session.query(Card).all()
    return jsonify(all_cards)


# @app.route("/card/<id>", methods = ['DELETE'])
# def delete_card():
#     database.delete_card(id)
#     return
