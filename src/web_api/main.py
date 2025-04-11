import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.domain.exceptions.duplicate_exception import DuplicateException
from .controllers import deck_controller, language_controller, account_controller, card_controller
from src.domain.entities import EntityBase
from src.infrastructure.database.database import db_engine
from src.domain.exceptions import DuplicateException, NotExistsException, FieldEmptyException, FieldTooLongException, TokenInvalidException, TokenExpiredException, WrongFileFormatException, TooFewCardsException
from .exception_handlers import duplicate_exception_handler, not_exists_exception_handler, field_empty_exception_handler, field_too_long_exception_handler, token_invalid_exception_handler, token_expired_exception_handler, wrong_file_format_exception_handler, too_few_cards_exception_handler
from alembic.config import Config
from alembic import command

# Initialize web_api with all controllers (routers)
app = FastAPI(title='Flashcards')
app.include_router(deck_controller.router)
app.include_router(card_controller.router)
app.include_router(language_controller.router)
app.include_router(account_controller.router)

# Add CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'https://flashcards-frontend-bice.vercel.app'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Generate database schema based on model classes
    EntityBase.metadata.create_all(db_engine)

    # TODO: Fix and uncomment
    # Run database migrations
    # config = Config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'infrastructure', 'database', 'alembic.ini')))
    # command.upgrade(config, "head")


# Handle our custom exceptions
app.add_exception_handler(DuplicateException, duplicate_exception_handler)
app.add_exception_handler(NotExistsException, not_exists_exception_handler)
app.add_exception_handler(FieldEmptyException, field_empty_exception_handler)
app.add_exception_handler(FieldTooLongException, field_too_long_exception_handler)
app.add_exception_handler(TokenInvalidException, token_invalid_exception_handler)
app.add_exception_handler(TokenExpiredException, token_expired_exception_handler)
app.add_exception_handler(WrongFileFormatException, wrong_file_format_exception_handler)
app.add_exception_handler(TooFewCardsException, too_few_cards_exception_handler)