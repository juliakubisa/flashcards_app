from fastapi import FastAPI, HTTPException
from src.domain.exceptions.duplicate_exception import DuplicateException
from src.domain.exceptions.not_exists_exception import NotExistsException
from .controllers import deck_controller
from src.domain.entities.model_base import ModelBase
from src.infrastructure.database.database import db_engine

app = FastAPI()
app.include_router(deck_controller.router)

# Generate database schema based on model classes
ModelBase.metadata.create_all(db_engine)

@app.exception_handler(DuplicateException)
async def duplicate_exception_handler(request, exc: DuplicateException):
    raise HTTPException(status_code=409, detail=str(exc))

@app.exception_handler(NotExistsException)
async def duplicate_exception_handler(request, exc: NotExistsException):
    raise HTTPException(status_code=404, detail=str(exc))


