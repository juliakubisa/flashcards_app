from pydantic import BaseModel


class CreateTokenRequest(BaseModel):
    email: str
    password: str