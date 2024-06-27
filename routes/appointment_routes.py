import logging
from fastapi import APIRouter, Request

from utils.common_utils import permission_required
from models.appointment_validation import AppoinmentModel
from controller.appointment_controller import AppointmentClient


router = APIRouter()
logger = logging.getLogger("log")


@router.post("/appointment/{patient_id}")
@permission_required("APPOINTMENT", "WRITE")
async def create_appointment(patient_id: str, app: AppoinmentModel, request: Request):
    logger.info(f"Request Payload: {patient_id}")
    return AppointmentClient.create_appointment(patient_id, app)


@router.get("/appointment")
@permission_required("APPOINTMENT", "READ")
async def get_all_appointment(request: Request):
    logger.info("Fetching all appointment")
    return AppointmentClient.get_all_appointment()



