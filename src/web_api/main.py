from fastapi import FastAPI, HTTPException
from src.domain.exceptions import DuplicateException, NotExistsException, FieldEmptyException, FieldTooLongException
from .controllers import deck_controller, language_controller, account_controller, card_controller
from src.domain.entities import EntityBase
from src.infrastructure.database.database import db_engine


# Initialize web_api with all controllers (routers)
app = FastAPI(title='Flashcards')
app.include_router(deck_controller.router, tags=['Decks'])
app.include_router(card_controller.router, tags=['Cards'])
app.include_router(language_controller.router, tags=['Languages'])
app.include_router(account_controller.router, tags=['Accounts'])

# TODO: include CORS settings here
# TODO: include migrations here

# Generate database schema based on model classes
EntityBase.metadata.create_all(db_engine)

# Handle our custom exceptions
@app.exception_handler(DuplicateException)
async def duplicate_exception_handler(request, exc: DuplicateException):
    raise HTTPException(status_code=409, detail=str(exc))

@app.exception_handler(NotExistsException)
async def not_exists_exception_handler(request, exc: NotExistsException):
    raise HTTPException(status_code=404, detail=str(exc))

@app.exception_handler(FieldTooLongException)
async def field_too_long_exception_handler(request, exc: FieldTooLongException):
    raise HTTPException(status_code=409, detail=str(exc))

@app.exception_handler(FieldEmptyException)
async def field_empty_exception_handler(request, exc: FieldEmptyException):
    raise HTTPException(status_code=400, detail=str(exc))