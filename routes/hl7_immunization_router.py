import logging
from fastapi import APIRouter, Request

from controller.hl7_immunization_controller import HL7ImmunizationClient


router = APIRouter()
logger = logging.getLogger("log")


@router.post('/vx04')
async def vx04_route(request: Request):
    raw_data = await request.body()
    logger.info("Request Payload: %s" % raw_data)
    response = HL7ImmunizationClient.create_immunization(raw_data)
    logger.info("Response: %s" % response)
    return response


@router.get("/immunization/{patient_id}")
async def get_immunizations_by_patient_id(patient_id: str):
    logger.info(f"Patient ID: {patient_id}")
    return HL7ImmunizationClient.get_immunizations_by_patient_id(patient_id)


@router.get("/immunization")
async def get_all_immunizations():
    logger.info("Get all immunizations")
    return HL7ImmunizationClient.get_all_immunizations()

