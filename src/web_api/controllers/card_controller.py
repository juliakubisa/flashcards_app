from fastapi import APIRouter

from src.application.commands.delete_card_command import DeleteCardCommand
from src.web_api.dependencies import CardRepositoryDependency


router = APIRouter()

@router.delete("/card/{card_id}", status_code=201)
async def delete_card(card_repository: CardRepositoryDependency, card_id: int):
    command = DeleteCardCommand(card_repository)
    command.handle(card_id)


@router.put("/card/{card_id}")
def update_card(card_id: int):
    pass
    # body = request.get_json()
    # does_card_exist = db.session.query(exists()
    #                                    .where(Card.foreign_word == body['foreign_word'])
    #                                    .where(Card.translated_word == body['translated_word'])
    #                                    .where(not_(Card.id == body['id']))).scalar()
    # condition, edited_card = edit_card_conditions(body, does_card_exist)
    # if condition is True:
    #     card_to_edit = Card.query.get(card_id)
    #     card_to_edit.foreign_word = body['foreign_word']
    #     card_to_edit.translated_word = body['translated_word']
    #     db.session.commit()
    #     return "Card edited", 200
    # else:
    #     return condition, 409



