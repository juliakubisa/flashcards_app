from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    name: str
    email: str
    password: str