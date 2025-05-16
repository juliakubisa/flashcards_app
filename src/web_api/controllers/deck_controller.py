from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import conint
from src.application.model.input import CreateCardRequest, CreateDeckRequest, CreateCardQuizLogRequest
from src.application.model.output import CreateCardResponse, CreateDeckResponse, DeckResponse, CardsPaginatedResponse, QuizCardResponse
from src.application.commands import CreateCardCommand, CreateDeckCommand, DeleteDeckCommand, CreateCardsFromFileCommand, UpdateDeckCommand, CreateCardQuizLogCommand
from src.application.queries import GetAllDecksQuery, GetCardsInDeckQuery, GetDeckQuery, GetQuizCardsQuery
from src.web_api.authentication_service import authenticate
from src.web_api.dependencies import CardRepositoryDependency, DeckRepositoryDependency, CardQuizLogRepositoryDependency


router = APIRouter(prefix="/decks", tags=['Decks'], dependencies=[Depends(authenticate)])

@router.get("")
async def get_all_decks(request: Request, deck_repository: DeckRepositoryDependency) -> list[DeckResponse]:
        query = GetAllDecksQuery(deck_repository)
        decks = query.handle(request.state.account_id)
        return decks


@router.get("/{deck_id}")
async def get_deck(request: Request, deck_repository: DeckRepositoryDependency, deck_id: int) -> DeckResponse:
    query = GetDeckQuery(deck_repository)
    deck = query.handle(deck_id, request.state.account_id)
    return deck


@router.post("", status_code=201)
async def create_deck(request: Request, deck_repository: DeckRepositoryDependency, deck: CreateDeckRequest) -> CreateDeckResponse:
     command = CreateDeckCommand(deck_repository)
     id_response = command.handle(deck, request.state.account_id)
     return id_response


@router.get("/{deck_id}/cards")
async def get_cards_in_deck(request: Request, 
                            card_repository: CardRepositoryDependency, 
                            deck_repository: DeckRepositoryDependency, 
                            deck_id: int,
                            page: conint(ge=0) = 0,
                            page_size: conint(ge=0) = 10,
                            search_text: str | None = None) -> CardsPaginatedResponse:
    query = GetCardsInDeckQuery(card_repository, deck_repository)
    cards = query.handle(deck_id, request.state.account_id, page, page_size, search_text)
    return cards


@router.delete("/{deck_id}", status_code=204)
async def delete_deck(request: Request, deck_repository: DeckRepositoryDependency, deck_id: int):
    command = DeleteDeckCommand(deck_repository)
    command.handle(deck_id, request.state.account_id)

@router.put("/{deck_id}", status_code=204)
async def update_deck(request: Request, 
                      deck_repository: DeckRepositoryDependency,
                      deck: CreateDeckRequest, deck_id: int):
    command = UpdateDeckCommand(deck_repository)
    command.handle(deck, deck_id, request.state.account_id)


@router.post("/{deck_id}/cards", status_code=201)
async def create_card(request: Request, 
                      card_repository: CardRepositoryDependency, 
                      deck_repository: DeckRepositoryDependency, deck_id: int, 
                      card: CreateCardRequest) -> CreateCardResponse:
    command = CreateCardCommand(card_repository, deck_repository)
    id_response = command.handle(deck_id, card, request.state.account_id)
    return id_response


@router.post("/{deck_id}/file", status_code=201)
async def create_cards_from_file(request: Request, 
                                card_repository: CardRepositoryDependency, 
                                deck_repository: DeckRepositoryDependency, 
                                deck_id: int, 
                                file: Annotated[UploadFile, File()],
                                delimiter: Annotated[str, Form()]) -> list[CreateCardResponse]:
    
    if file is None:
        raise HTTPException(400, "File is required")

    if file.size > 10 * 1024 * 1024: # 10 MB
        raise HTTPException(413, "File too large (max size is 10 MB)")

    if not file.filename.endswith(".txt") and not file.filename.endswith(".csv"):
        raise HTTPException(400, "Unsupported file extension")
    
    try:   
        file_content = (await file.read()).decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File contains an illegal non-unicode character")
    
    command = CreateCardsFromFileCommand(card_repository, deck_repository)
    ids_response = command.handle(deck_id, file_content, delimiter, request.state.account_id)
    
    return ids_response

@router.get("/{deck_id}/quiz/cards")
async def get_quiz_cards(request: Request, 
                         card_repository: CardRepositoryDependency, 
                         deck_repository: DeckRepositoryDependency,
                         deck_id: int, 
                         number_of_cards: int) -> list[QuizCardResponse]:
    query = GetQuizCardsQuery(card_repository, deck_repository)
    cards = query.handle(deck_id, number_of_cards, request.state.account_id)
    return cards


@router.post("/{deck_id}/quiz/results")
async def create_card_quiz_logs(request: Request,
                                card_quiz_log_repository: CardQuizLogRepositoryDependency,
                                deck_repository: DeckRepositoryDependency,
                                card_repository: CardRepositoryDependency,
                                card_quiz_log: CreateCardQuizLogRequest,
                                deck_id = int):
    command = CreateCardQuizLogCommand(card_quiz_log_repository, deck_repository, card_repository)
    id_response = command.handle(deck_id, card_quiz_log, request.state.account_id)
    return id_response
