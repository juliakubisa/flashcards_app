from fastapi import HTTPException
from src.domain.exceptions import DuplicateException, NotExistsException, FieldEmptyException, FieldTooLongException, TokenInvalidException, TokenExpiredException, WrongFileFormatException


async def duplicate_exception_handler(request, exc: DuplicateException):
    raise HTTPException(status_code=409, detail=str(exc))

async def not_exists_exception_handler(request, exc: NotExistsException):
    raise HTTPException(status_code=404, detail=str(exc))

async def field_too_long_exception_handler(request, exc: FieldTooLongException):
    raise HTTPException(status_code=409, detail=str(exc))

async def field_empty_exception_handler(request, exc: FieldEmptyException):
    raise HTTPException(status_code=400, detail=str(exc))

async def token_invalid_exception_handler(request, exc: TokenInvalidException):
    raise HTTPException(status_code=401, detail=str(exc))

async def token_expired_exception_handler(request, exc: TokenExpiredException):
    raise HTTPException(status_code=401, detail=str(exc))

async def wrong_file_format_exception_handler(request, exc: WrongFileFormatException):
    raise HTTPException(status_code=400, detail=str(exc))