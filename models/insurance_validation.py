from pydantic import BaseModel


class InsuranceModel(BaseModel):
    name: str
    alias: list
