import logging
from fastapi import APIRouter, Request

from models.patient_validation import PatientModel
from services.patient_service import PatientService
from utils.common_utils import permission_required

router = APIRouter()
logger = logging.getLogger("log")


@router.post("/patient")
@permission_required("PATIENT", "WRITE")
async def patient_route(pat: PatientModel, request: Request):
    logger.info(f"Request Payload: {pat}")
    response = PatientService.create_patient(pat)
    logger.info(f"Request Payload: {response}")
    return response


@router.get("/patients/{patient_id}")
@permission_required("PATIENT", "READ")
async def get_patient(patient_id: str, request: Request):
    logger.info(f"Patient ID:{patient_id}")
    return PatientService.get_patient_by_id(patient_id)


@router.get("/patients")
@permission_required("PATIENT", "READ")
async def get_all_patients(request: Request):
    logger.info("Fetching all patients")
    return PatientService.get_all_patients()


@router.delete("/patients/{patient_id}")
@permission_required("PATIENT", "DELETE")
async def delete_patient(patient_id: str, request: Request):
    logger.info(f"Deleting patient ID:{patient_id}")
    return PatientService.delete_patient_by_id(patient_id)
