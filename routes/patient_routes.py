import logging
from fastapi import APIRouter

from models.patient_validation import PatientModel
from services.patient_service import PatientService

router = APIRouter()
logger = logging.getLogger("log")


@router.post('/patient')
async def patient_route(pat: PatientModel):
    logger.info(f"Request Payload: {pat}")
    response = PatientService.create_patient(pat)
    logger.info(f"Request Payload: {response}")
    return response


@router.get("/patients/{patient_id}")
async def get_patient(patient_id: str):
    logger.info(f"Patient ID:{patient_id}")
    return PatientService.get_patient_by_id(patient_id)


@router.get("/patients")
async def get_all_patients():
    logger.info("Fetching all patients")
    return PatientService.get_all_patients()


@router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: str):
    logger.info(f"Deleting patient ID:{patient_id}")
    return PatientService.delete_patient_by_id(patient_id)




