from fastapi import APIRouter
from src.application.commands import DeleteCardCommand, UpdateCardCommand
from src.application.model.input.create_card_request import CreateCardRequest
from src.web_api.dependencies import CardRepositoryDependency


router = APIRouter(prefix="/cards", tags=['Cards'])

@router.delete("/{card_id}", status_code=204)
async def delete_card(card_repository: CardRepositoryDependency, card_id: int):
    command = DeleteCardCommand(card_repository)
    command.handle(card_id)


@router.put("/{card_id}", status_code = 204)
async def update_card(card_repository: CardRepositoryDependency, request: CreateCardRequest, card_id: int):
    command = UpdateCardCommand(card_repository)
    command.handle(request, card_id)