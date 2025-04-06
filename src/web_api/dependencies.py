from fastapi import Depends
from src.infrastructure.database.database import LocalSession
from sqlalchemy.orm import Session
from typing import Annotated
from src.infrastructure.database.repositories.card_repository import CardRepository
from src.infrastructure.database.repositories.deck_repository import DeckRepository

# Ensures there is always a separate db session for each request
def create_db_session():
    with LocalSession() as session:
        yield session

DatabaseSession = Annotated[Session, Depends(create_db_session)]

def create_deck_repository(db_session: DatabaseSession) -> DeckRepository:
    return DeckRepository(db_session)

DeckRepositoryDependency = Annotated[DeckRepository, Depends(create_deck_repository)]

def create_card_repository(db_session: DatabaseSession) -> CardRepository:
    return CardRepository(db_session)

CardRepositoryDependency = Annotated[CardRepository, Depends(create_card_repository)]

