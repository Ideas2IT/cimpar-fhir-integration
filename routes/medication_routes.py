from fastapi import APIRouter, Request

from models.medication_validation import MedicationCreateModel, MedicationUpdateModel
from services.medication_service import MedicationService
from utils.common_utils import permission_required

router = APIRouter()


@router.post("/medications", response_model=dict)
@permission_required("MEDICATION", "WRITE")
async def create_medication(med: MedicationCreateModel, request: Request):
    print("medication route", med)
    return MedicationService.create_medication(med)


@router.get("/medication/{patient_id}")
@permission_required("MEDICATION", "READ")
def get_medication_by_patient_id(patient_id: str, request: Request):
    return MedicationService.get_medication_by_patient_id(patient_id)


@router.put("/medication/{patient_id}")
@permission_required("MEDICATION", "UPDATE")
async def update_medication(patient_id: str, updated_medication: MedicationUpdateModel, request: Request):
    return MedicationService.update_medication_by_patient_id(patient_id, updated_medication)

