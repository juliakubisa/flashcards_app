from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from src.application.model.input import CreateCardRequest, CreateDeckRequest
from src.application.model.output import CreateCardResponse, CreateDeckResponse, DeckResponse, CardResponse
from src.application.commands import CreateCardCommand, CreateDeckCommand, DeleteDeckCommand, CreateCardsFromFileCommand
from src.application.queries import GetAllDecksQuery, GetCardsInDeckQuery, GetDeckQuery
from src.web_api.authentication_service import authenticate
from src.web_api.dependencies import CardRepositoryDependency, DeckRepositoryDependency


router = APIRouter(prefix="/decks", tags=['Decks'], dependencies=[Depends(authenticate)])

@router.get("")
async def get_all_decks(deck_repository: DeckRepositoryDependency) -> list[DeckResponse]:
        query = GetAllDecksQuery(deck_repository)
        decks = query.handle()
        return decks


@router.get("/{deck_id}")
async def get_deck(deck_repository: DeckRepositoryDependency, deck_id: int) -> DeckResponse:
    query = GetDeckQuery(deck_repository)
    deck = query.handle(deck_id)
    return deck


@router.post("", status_code=201)
async def create_deck(deck_repository: DeckRepositoryDependency, deck: CreateDeckRequest) -> CreateDeckResponse:
     command = CreateDeckCommand(deck_repository)
     id_response = command.handle(deck)
     return id_response


@router.get("/{deck_id}/cards")
async def get_cards_in_deck(card_repository: CardRepositoryDependency, deck_id: int) -> list[CardResponse]:
    query = GetCardsInDeckQuery(card_repository)
    cards = query.handle(deck_id)
    return cards


@router.delete("/{deck_id}", status_code=204)
async def delete_deck(deck_repository: DeckRepositoryDependency, deck_id: int):
    command = DeleteDeckCommand(deck_repository)
    command.handle(deck_id)


@router.post("/{deck_id}/cards", status_code=201)
async def create_card(card_repository: CardRepositoryDependency, 
                      deck_repository: DeckRepositoryDependency, deck_id: int, 
                      card: CreateCardRequest) -> CreateCardResponse:
    command = CreateCardCommand(card_repository, deck_repository)
    id_response = command.handle(deck_id, card)
    return id_response


@router.post("/{deck_id}/file", status_code=201)
async def create_cards_from_file(card_repository: CardRepositoryDependency, 
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
    ids_response = command.handle(deck_id, file_content, delimiter)
    
    return ids_response

# @router.route("/decks/<deck_id>/quiz/cards", methods=['GET'])
# def return_quiz_cards(deck_id):
#     all_cards = db.session.query(Deck).filter(Deck.id == deck_id).options(joinedload(Deck.cards)).first().cards
#     num_cards = int(request.args.get('number_of_cards'))
#     if len(all_cards) >= num_cards and len(all_cards) >= 10:
#         algorithm = Algorithm(all_cards, num_cards)
#         algorithm.set_weights()
#         cards_to_quiz = algorithm.select_quiz_cards()
#         return jsonify([card.__dict__ for card in cards_to_quiz])
#     else:
#         return "Too few cards to quiz", 400


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
