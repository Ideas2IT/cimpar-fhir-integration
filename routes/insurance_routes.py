from fastapi import APIRouter
import logging

from models.insurance_validation import InsuranceModel
from services.insurance_service import InsuranceService

router = APIRouter()
logger = logging.getLogger("log")


@router.post('/insurance')
async def insurance_route(ins_plan: InsuranceModel):
    logger.info(f"Request Payload: {ins_plan}")
    response = InsuranceService.create_insurance(ins_plan)
    logger.info(f"Request Payload: {response}")
    return response

