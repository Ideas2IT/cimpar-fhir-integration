from fastapi import APIRouter
import logging

from models.insurance_validation import CoverageModel, CoverageUpdateModel
from services.insurance_service import InsuranceService

router = APIRouter()
logger = logging.getLogger("log")


@router.post('/insurance')
async def insurance_route(ins_plan: CoverageModel):
    logger.info(f"Request Payload: {ins_plan}")
    response = InsuranceService.create_insurance(ins_plan)
    logger.info("Response: %s" % response)
    return response


@router.get('/insurance/{patient_id}')
async def get_insurance_by_patient_id(patient_id: str):
    logger.info(f"Request Patient_id: {patient_id}")
    return InsuranceService.get_insurance_by_patient_id(patient_id)

@router.put('/insurance/{patient_id}')
async def update_insurance(patient_id: str, updated_insurance: CoverageUpdateModel):
    logger.info(f"Request Patient_id: {patient_id}")
    return InsuranceService.update_insurance_by_patient_id(patient_id, updated_insurance)

@router.delete('/insurance/{patient_id}')
async def delete_insurance(patient_id: str):
    logger.info(f"Request Patient_id: {patient_id}")
    return InsuranceService.delete_insurance_by_patient_id(patient_id)
