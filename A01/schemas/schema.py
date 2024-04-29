from pydantic import BaseModel
from typing import List, Optional

class Identifier(BaseModel):
    id: Optional[str]
    value: Optional[str]
    type: Optional[str]
    system: Optional[str]

class PhoneNumber(BaseModel):
    use: str
    system: str
    value: str

class Patient(BaseModel):
    home_phone: PhoneNumber
    patient_id: Identifier
    ssn_number: Optional[str]
    identifiers: List[Identifier]