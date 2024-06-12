from fastapi import APIRouter, Request

from models.medication_validation import MedicationCreateModel, MedicationUpdateModel
from controller.medication_controller import MedicationClient


router = APIRouter()

@router.post("/medication", response_model=dict)
async def create_medication(med: MedicationCreateModel):
    return MedicationClient.create_medication(med)


@router.get("/medication/{patient_id}")
async def get_medication_by_patient_id(patient_id: str):
    return MedicationClient.get_medication_by_patient_id(patient_id)


@router.put("/medication/{patient_id}")
async def update_medication(updated_medication: MedicationUpdateModel):
    return MedicationClient.update_medication_by_patient_id(updated_medication)

