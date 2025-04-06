from pydantic import BaseModel


class LanguageResponse(BaseModel):
    id: str
    name: str
