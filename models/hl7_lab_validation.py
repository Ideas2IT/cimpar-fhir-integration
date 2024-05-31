from pydantic import BaseModel


class ORUModel(BaseModel):
    message: str