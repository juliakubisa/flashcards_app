from pydantic import BaseModel


class CreateCardQuizLogResponse(BaseModel):
    id: int