from pydantic import BaseModel


class CreateDeckRequest(BaseModel):
    name: str
    language_id: str
