import json
from flask import Flask
from src.application.database import Database

app = Flask(__name__)

@app.route("/cards")
def return_cards():
    database = Database()
    all_cards = database.get_cards()
    return json.dumps(all_cards)


# @app.route("/card", method = POST)
# def get_cards():
#     database.delete_card(id)
#
#     return
