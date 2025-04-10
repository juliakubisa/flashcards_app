from pydantic import BaseModel


class CreateCardResponse(BaseModel):
    id: int