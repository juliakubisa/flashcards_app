from pydantic import BaseModel


class CreateDeckResponse(BaseModel):
    id: int