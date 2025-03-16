from flask import *
import os
from flask_cors import CORS
from src.application.utils import create_default_deck
from src.web_api.controllers import account_controller, card_controller, deck_controller, language_controller
from src.application.sql_database import db
from src.application.update_languages_table import insert_languages
from flask_migrate import Migrate


app = Flask(__name__)

CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_CONNECTION_STRING']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # restrict max size to 16MB
app.config['JWT_SECRET'] = os.environ['JWT_SECRET']
app.config['GOOGLE_CLIENT_ID'] = os.environ['GOOGLE_CLIENT_ID']

db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()
    migrate = Migrate(app, db)
    insert_languages(db.session)

app.register_blueprint(card_controller.card_controller)
app.register_blueprint(deck_controller.deck_controller)
app.register_blueprint(language_controller.language_controller)
app.register_blueprint(account_controller.account_controller)

