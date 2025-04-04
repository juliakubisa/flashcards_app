from fastapi import FastAPI, HTTPException
from src.domain.exceptions.duplicate_exception import DuplicateException
from .controllers import deck_controller, language_controller
from src.domain.entities.model_base import ModelBase
from src.infrastructure.database.database import db_engine


# Initialize web_api with all controllers (routers)
app = FastAPI(title='Flashcards')
app.include_router(deck_controller.router, tags=['Decks'])
app.include_router(language_controller.router, tags=['Languages'])

# TODO: include CORS settings here
# TODO: include migrations here

# Generate database schema based on model classes
ModelBase.metadata.create_all(db_engine)

# Handle our custom exceptions
@app.exception_handler(DuplicateException)
async def duplicate_exception_handler(request, exc: DuplicateException):
    raise HTTPException(status_code=409, detail=str(exc))