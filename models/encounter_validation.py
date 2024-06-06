from pydantic import BaseModel


class EncounterModel(BaseModel):
    location: str 
    phone_number: str
    admission_date: str
    discharge_date: str
    reason: str
    primary_care_team: str
    treatment_summary: str
    status: str
    class_code: str
    patient_id: str

class EncounterUpdateModel(BaseModel):
    id: str
    location: str 
    phone_number: str
    admission_date: str
    discharge_date: str
    reason: str
    primary_care_team: str
    treatment_summary: str
    status: str
    class_code: str
    patient_id: str
    

