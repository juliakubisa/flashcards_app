from fastapi import Depends
from src.infrastructure.database.database import LocalSession
from sqlalchemy.orm import Session
from typing import Annotated
from src.infrastructure.database.repositories import CardRepository, DeckRepository, LanguageRepository
from src.infrastructure.database.repositories.account_repository import AccountRepository
from src.infrastructure.services import JWTTokenService, GoogleAuthService, ImageStorageService
from src.web_api.settings import Settings

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

# AccountRepository
def create_account_repository(db_session: DatabaseSession) -> AccountRepository:
    return AccountRepository(db_session)

AccountRepositoryDependency = Annotated[AccountRepository, Depends(create_account_repository)]

# JWTTokenService
def create_jwt_token_service() -> JWTTokenService:
    settings = Settings.load()
    return JWTTokenService(settings.jwt_secret, settings.access_token_age_seconds, settings.refresh_token_age_seconds)

JWTTokenServiceDependency = Annotated[JWTTokenService, Depends(create_jwt_token_service)]

# GoogleAuthService
def create_google_auth_service() -> GoogleAuthService:
    google_client_id = Settings.load().google_client_id
    return GoogleAuthService(google_client_id)

GoogleAuthServiceDependency = Annotated[GoogleAuthService, Depends(create_google_auth_service)]

# ImageStorageService
def create_image_storage_service() -> ImageStorageService:
    settings = Settings.load()
    return ImageStorageService(settings.aws_access_key_id, settings.aws_secret_access_key, settings.access_token_age_seconds)

ImageStorageServiceDependency = Annotated[ImageStorageService, Depends(create_image_storage_service)]