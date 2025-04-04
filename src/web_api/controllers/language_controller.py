from flask import *
from src.domain.entities.language import Language
from src.application.sql_database import db

language_controller = Blueprint('language_controller', __name__)

@language_controller.route("/languages", methods=['GET'])
def return_languages():
    all_languages = db.session.query(Language).all()
    return jsonify(all_languages)