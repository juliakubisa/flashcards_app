from flask import *
import os
from src.web_api.controllers import card_controller
from src.application.sql_database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_CONNECTION_STRING']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # restrict max size to 16MB

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(card_controller.card_controller)