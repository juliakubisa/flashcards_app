from fastapi import APIRouter, HTTPException
from src.application.commands.create_card_command import CreateCardCommand
from src.application.commands.create_deck_command import CreateDeckCommand
from src.application.commands.delete_deck_command import DeleteDeckCommand
from src.application.model.input.create_card_request import CreateCardRequest
from src.application.model.input.create_deck_request import CreateDeckRequest
from src.application.model.output.create_card_response import CreateCardResponse
from src.application.model.output.create_deck_response import CreateDeckResponse
from src.application.model.output.deck_response import DeckResponse
from src.application.model.output.card_response import CardResponse
from src.application.queries.get_all_decks_query import GetAllDecksQuery
from src.application.queries.get_cards_query import GetCardsInDeckQuery
from src.application.queries.get_deck_query import GetDeckQuery
from src.web_api.dependencies import CardRepositoryDependency, DeckRepositoryDependency


router = APIRouter()

@router.get("/decks")
async def get_all_decks(deck_repository: DeckRepositoryDependency) -> list[DeckResponse]:
        query = GetAllDecksQuery(deck_repository)
        decks = query.handle()
        return decks


@router.get("/decks/{deck_id}")
async def get_deck(deck_repository: DeckRepositoryDependency, deck_id: int) -> DeckResponse:
    if deck_id is None:
        raise HTTPException(status_code=400, detail="Deck ID is required")

    query = GetDeckQuery(deck_repository)
    deck = query.handle(deck_id)
    
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
   
    return deck

@router.post("/decks", status_code=200)
async def create_deck(deck_repository: DeckRepositoryDependency, deck: CreateDeckRequest) -> CreateDeckResponse:
     if deck.name is None:
        raise HTTPException(status_code=400, detail="Deck name is required")
     if deck.language_id is None:
        raise HTTPException(status_code=400, detail="Deck language is required")

     command = CreateDeckCommand(deck_repository)
     id_response = command.handle(deck)
     return id_response


@router.get("/decks/{deck_id}/cards")
async def get_cards_in_deck(card_repository: CardRepositoryDependency, deck_id: int) -> list[CardResponse]:
    query = GetCardsInDeckQuery(card_repository)
    cards = query.handle(deck_id)
    return cards

@router.delete("/decks/{deck_id}", status_code=201)
async def delete_deck(deck_repository: DeckRepositoryDependency, deck_id: int):
    command = DeleteDeckCommand(deck_repository)
    command.handle(deck_id)


@router.post("/decks/{deck_id}/cards")
async def add_card(card_repository: CardRepositoryDependency, deck_repository: DeckRepositoryDependency, deck_id: int, card: CreateCardRequest) -> CreateCardResponse:
    command = CreateCardCommand(card_repository, deck_repository)
    id_response = command.handle(deck_id, card)
    return id_response



# @router.route("/decks/<deck_id>/file", methods=['POST'])
# def upload_cards_from_file(deck_id):
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'No selected file', 400
#         file = request.files['file']
#         if file.filename == '':
#             return 'No selected file', 400
#         if not allowed_file_extension(file.filename):
#             return 'Unsupported file extension', 400
#         if file and allowed_file_extension(file.filename):
#             raw_data = StringIO(file.stream.read().decode("UTF8"), newline=None)
#             delimiter = request.form['delimiter']
#             cards_unknown_unique = read_input_file(raw_data, deck_id, delimiter)
#             db.session.add_all(cards_unknown_unique)
#             db.session.commit()
#             return 'Cards added', 200


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
