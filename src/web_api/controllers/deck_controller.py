from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import conint
from src.application.model.input import CreateCardRequest, CreateDeckRequest
from src.application.model.output import CreateCardResponse, CreateDeckResponse, DeckResponse, CardsPaginatedResponse, QuizCardResponse
from src.application.commands import CreateCardCommand, CreateDeckCommand, DeleteDeckCommand, CreateCardsFromFileCommand, UpdateDeckCommand
from src.application.queries import GetAllDecksQuery, GetCardsInDeckQuery, GetDeckQuery, GetQuizCardsQuery
from src.domain.enums import SortCardsBy, SortDirection, SortDecksBy
from src.web_api.authentication_service import authenticate
from src.web_api.dependencies import CardRepositoryDependency, DeckRepositoryDependency


router = APIRouter(prefix="/decks", tags=['Decks'], dependencies=[Depends(authenticate)])

@router.get("")
async def get_all_decks(request: Request, 
                        deck_repository: DeckRepositoryDependency,
                        search_text: str | None = None,
                        sort_by: SortDecksBy = SortDecksBy.NAME,
                        sort_direction: SortDirection = SortDirection.ASCENDING) -> list[DeckResponse]:
        query = GetAllDecksQuery(deck_repository)
        decks = query.handle(request.state.account_id, search_text, sort_by, sort_direction)
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
                            search_text: str | None = None,
                            sort_by: SortCardsBy = SortCardsBy.DATE_ADDED,
                            sort_direction: SortDirection = SortDirection.DESCENDING) -> CardsPaginatedResponse:
    query = GetCardsInDeckQuery(card_repository, deck_repository)
    cards = query.handle(deck_id, request.state.account_id, page, page_size, search_text, sort_by, sort_direction)
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



# @router.route("/decks/<deck_id>/quiz/results", methods=['PUT'])
# def update_card_statistics(deck_id):
#     body = request.get_json()
#     date_now = date.today()

#     # Update only the cards that were quizzed
#     ids_to_update = [card['id'] for card in body]
#     cards_to_update = db.session.query(Card).filter(Card.id.in_(ids_to_update)).all()

#     for card in cards_to_update:
#         # Replace the old data with the new data from quiz for each card
#         new_data = next((data for data in body if data["id"] == card.id), None)

#         card.date_last_review = date_now
#         card.answer_time = new_data['answer_time_ms']
#         card.last_answer_correct = new_data['last_answer_correct']

#         if new_data['last_answer_correct']:
#             card.number_correct_answers = card.number_correct_answers + 1

#     db.session.commit()
#     return "Statistics updated", 200
