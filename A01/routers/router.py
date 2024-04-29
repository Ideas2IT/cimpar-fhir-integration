from fastapi import APIRouter
from A01.schemas.schema import Patient

router = APIRouter()


@router.post("/patient", response_model=Patient)
async def create_patient(patient: Patient):
    return {"patient_id": patient.patient_id, "patient": patient}

@router.get("/patient/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str):
    return Patient(patient_id=patient_id, home_phone={"use": "home", "system": "phone", "value": "555-555-5555"}, ssn_number="123-45-6789", identifiers=[{"id": "1", "value": "12345", "type": "MRN", "system": "EHR"}])

@router.put("/patient/{patient_id}", response_model=Patient)
async def update_patient(patient_id: str, patient: Patient):
    return patient

@router.delete("/patient/{patient_id}")
async def delete_patient(patient_id: str):
    return {"message": "Patient deleted successfully"}