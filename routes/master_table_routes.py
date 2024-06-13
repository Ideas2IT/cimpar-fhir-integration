import logging
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBearer

from controller.medication_list_controller import MedicationList

router = APIRouter()
logger = logging.getLogger("log")


@router.get("/medication_list/{medication_name}")
async def get_medication_list(medication_name: str):
    if len(medication_name) <= 2:
        logger.info("Medication name must be at least 2 characters long.")
        return None
    logger.info(f"Medication Name:{medication_name}")
    return MedicationList.get_medication_list(medication_name)

@router.get("/allergy_list/{allergy_name}")
async def get_allergy_list(allergy_name: str):
    if len(allergy_name) <= 2:
        logger.info("Allergy name must be at least 2 characters long.")
        return None
    logger.info(f"Allergy Name:{allergy_name}")
    return MedicationList.get_allergy_list(allergy_name)