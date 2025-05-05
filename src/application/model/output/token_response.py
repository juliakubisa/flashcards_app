from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    email: str
    name: str
    image_url: str | None = None
