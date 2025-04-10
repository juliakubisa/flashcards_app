from pydantic import BaseModel


class CreateTokenWithGoogleRequest(BaseModel):
    id_token: str