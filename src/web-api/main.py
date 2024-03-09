import json

from flask import Flask
from src.application.input import read_input_file

app = Flask(__name__)


@app.route("/cards")
def get_cards():
    cards = read_input_file('example_words.csv')

    return json.dumps([obj.__dict__ for obj in cards])