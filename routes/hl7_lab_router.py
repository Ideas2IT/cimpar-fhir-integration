from fastapi import APIRouter, Request
import logging

from services.hl7_lab_service import HL7LabService

router = APIRouter()
logger = logging.getLogger("log")


@router.post('/oru')
async def oru_route(request: Request):
    raw_data = await request.body()
    logger.info("Request Payload: %s" % raw_data)
    response = HL7LabService.create_vx04(raw_data)
    logger.info("Response: %s" % response)
    return response


