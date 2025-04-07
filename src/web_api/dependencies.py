from fastapi import Depends
from src.infrastructure.database.database import LocalSession
from sqlalchemy.orm import Session
from typing import Annotated
from src.infrastructure.database.repositories import CardRepository, DeckRepository, LanguageRepository

# DatabaseSession
# Ensures there is always a separate db session for each request
def create_db_session():
    with LocalSession() as session:
        yield session

DatabaseSession = Annotated[Session, Depends(create_db_session)]

# DeckRepository
def create_deck_repository(db_session: DatabaseSession) -> DeckRepository:
    return DeckRepository(db_session)

DeckRepositoryDependency = Annotated[DeckRepository, Depends(create_deck_repository)]

# CardRepository
def create_card_repository(db_session: DatabaseSession) -> CardRepository:
    return CardRepository(db_session)

CardRepositoryDependency = Annotated[CardRepository, Depends(create_card_repository)]

# LanguageRepository
def create_language_repository(db_session: DatabaseSession) -> LanguageRepository:
    return LanguageRepository(db_session)

LanguageRepositoryDependency = Annotated[LanguageRepository, Depends(create_language_repository)]

