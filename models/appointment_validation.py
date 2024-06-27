from typing import List
from pydantic import BaseModel

class Concept(BaseModel):
    code: str
    system: str
    display: str

class AppoinmentModel(BaseModel):
    status: str
    participant_status: str
    test_to_take: str
    date_of_appoinment: str
    schedule_time: str
    reason_for_test: str
    other_reason: str
    current_medication: List[Concept]
    other_medication: List[Concept]
    current_allergy: List[Concept]