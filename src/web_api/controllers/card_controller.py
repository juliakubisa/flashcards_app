from fastapi import APIRouter, Depends, Request
from src.application.commands import DeleteCardCommand, UpdateCardCommand
from src.application.model.input.create_card_request import CreateCardRequest
from src.web_api.authentication_service import authenticate
from src.web_api.dependencies import CardRepositoryDependency, DeckRepositoryDependency


router = APIRouter(prefix="/cards", tags=['Cards'], dependencies=[Depends(authenticate)])

@router.delete("/{card_id}", status_code=204)
async def delete_card(request: Request, 
                      card_repository: CardRepositoryDependency, 
                      deck_repository: DeckRepositoryDependency, 
                      card_id: int):
    command = DeleteCardCommand(card_repository, deck_repository)
    command.handle(card_id, request.state.account_id)


@router.put("/{card_id}", status_code = 204)
async def update_card(request: Request, 
                      card_repository: CardRepositoryDependency, 
                      deck_repository: DeckRepositoryDependency, 
                      card: CreateCardRequest, card_id: int):
    command = UpdateCardCommand(card_repository, deck_repository)
    command.handle(card, card_id, request.state.account_id)