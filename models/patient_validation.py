from typing import Optional
from pydantic import BaseModel


class PatientModel(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    gender: str
    date_of_birth: str
    phone_number: str
    city: str
    zip_code: str
    full_address: str
    state: str
    country: str
    email: str
    height: str
    weight: str
