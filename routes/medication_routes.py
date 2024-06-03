from fastapi import APIRouter

from models.medication_validation import MedicationCreateModel, MedicationUpdateModel
from services.medication_service import MedicationService

router = APIRouter()

@router.post("/medications", response_model=dict)
async def create_medication(med: MedicationCreateModel):
    print("medication route", med)
    return MedicationService.create_medication(med)

@router.get("/medication/{patient_id}")
def get_medication_by_patient_id(patient_id: str):
    return MedicationService.get_medication_by_patient_id(patient_id)

@router.put("/medication/{patient_id}")
async def update_medication(patient_id: str, updated_medication: MedicationUpdateModel):
    return MedicationService.update_medication_by_patient_id(patient_id, updated_medication)

