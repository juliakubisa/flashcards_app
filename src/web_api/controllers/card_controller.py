# from flask import *
# from sqlalchemy import exists, not_
# from src.domain.entities.card import Card
# from src.application.sql_database import db
# from src.web_api.controllers.utils import add_card_conditions, edit_card_conditions

# card_controller = Blueprint('card_controller', __name__)

# @card_controller.route("/card/<card_id>", methods=['DELETE'])
# def delete_card(card_id):
#     card_to_delete = Card.query.get(card_id)
#     db.session.delete(card_to_delete)
#     db.session.commit()
#     return "Card deleted", 200


# @card_controller.route("/card/<card_id>", methods=['PUT'])
# def edit_card(card_id):
#     body = request.get_json()
#     does_card_exist = db.session.query(exists()
#                                        .where(Card.foreign_word == body['foreign_word'])
#                                        .where(Card.translated_word == body['translated_word'])
#                                        .where(not_(Card.id == body['id']))).scalar()
#     condition, edited_card = edit_card_conditions(body, does_card_exist)
#     if condition is True:
#         card_to_edit = Card.query.get(card_id)
#         card_to_edit.foreign_word = body['foreign_word']
#         card_to_edit.translated_word = body['translated_word']
#         db.session.commit()
#         return "Card edited", 200
#     else:
#         return condition, 409



