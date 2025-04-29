from pydantic import BaseModel
from .card_response import CardResponse

class CardsPaginatedResponse(BaseModel):
    items: list[CardResponse]
    page: int
    page_size: int
    total: int
    