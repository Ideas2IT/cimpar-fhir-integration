from fastapi import APIRouter, Request
import logging

from models.hl7_immunization_validation import VXO4Model
from services.hl7_immunization_service import HL7ImmunizationService

router = APIRouter()
logger = logging.getLogger("log")


@router.post('/vx04')
async def vx04_route(request: Request):
    raw_data = await request.body()
    logger.info("Request Payload: %s" % raw_data)
    response = HL7ImmunizationService.create_vx04(raw_data)
    logger.info("Response: %s" % response)
    return response

