from src.application.model.output import CreateCardResponse
from src.domain.entities import Card
from src.domain.exceptions import WrongFileFormatException, FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import CardRepository, DeckRepository

class CreateCardsFromFileCommand:
    def __init__(self, card_repository: CardRepository, deck_repository: DeckRepository):
        self.card_repository = card_repository
        self.deck_repository = deck_repository

    def handle(self, deck_id: int, file_content: str, delimiter: str, account_id: int) -> list[CreateCardResponse]:
        if deck_id is None:
            raise FieldEmptyException("Deck ID is required")
        
        if len(file_content) == 0:
            raise FieldEmptyException("File cannot be empty")
        
        existing_deck = self.deck_repository.get_by_id(deck_id)

        if existing_deck is None or existing_deck.account_id != account_id: 
            raise NotExistsException("Deck not found")
        
        lines = file_content.strip().splitlines()

        cards_to_add: list[Card] = []

        for line in lines:
            if delimiter in line:
                try:
                    word_pair = line.strip().split(delimiter)
                    foreign_word = word_pair[0].replace('"', '').strip()
                    translated_word = word_pair[1].replace('"', '').strip()
                except:
                    raise WrongFileFormatException('Wrong file format')
                
                if any(c.foreign_word == foreign_word and c.translated_word == translated_word for c in cards_to_add):
                    continue

                card = Card(foreign_word=foreign_word, translated_word=translated_word, deck_id=deck_id)
                cards_to_add.append(card)

        ids = self.card_repository.add_many(cards_to_add)
        return [CreateCardResponse(id=id) for id in ids]
        

 