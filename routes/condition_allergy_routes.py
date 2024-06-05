import logging
from fastapi import APIRouter

from models.condition_validation import ConditionModel, ConditionUpdateModel
from services.condition_allergy_service import ConditionAllergyService

router = APIRouter()
logger = logging.getLogger("log")

@router.post("/condition_allergy")
async def create_condition_allergy(condition: ConditionModel):
    logger.info(f"Request Payload: {condition}")
    response = ConditionAllergyService.create_condition_allergy(condition)
    logger.info(f"Response Payload: {response}")
    return response


@router.get("/condition_allergy")
async def get_condition_allergy(patient_id: str):
    response = ConditionAllergyService.get_condition_allergy(patient_id)
    logger.info(f"Response Payload: {response}")
    return response

@router.put("/condition_allergy")
async def update_condition_allergy(patient_id: str, condition: ConditionUpdateModel):
    logger.info(f"Request Payload: {condition}")
    response = ConditionAllergyService.update_condition_allergy(patient_id, condition)
    logger.info(f"Response Payload: {response}")
    return response