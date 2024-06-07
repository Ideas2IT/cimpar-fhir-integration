import logging
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer

from models.encounter_validation import EncounterModel, EncounterUpdateModel
from controller.encounter_controller import EncounterClient
from utils.common_utils import permission_required


router = APIRouter()
logger = logging.getLogger("log")

sec_scheme = HTTPBearer()

@router.post("/encounter", dependencies=[Depends(sec_scheme)])
@permission_required("ENCOUNTER", "WRITE")
async def create_encounter(encounter: EncounterModel, request: Request):
    logger.info(f"Request Payload: {encounter}")
    response = EncounterClient.create_encounter(encounter)
    logger.info(f"Response Payload: {response}")
    return response


@router.get("/encounter/{encounter_id}")
@permission_required("ENCOUNTER", "READ")
async def get_encounter(encounter_id: str, request: Request):
    logger.info(f"Encounter ID:{encounter_id}")
    return EncounterClient.get_encounter_by_id(encounter_id)


@router.get("/encounter")
@permission_required("ENCOUNTER", "READ")
async def get_all_encounters():
    logger.info("Fetching all encounters")
    return EncounterClient.get_all_encounters()

@router.put("/encounter/{encounter_id}")
@permission_required("ENCOUNTER", "EDIT")
async def update_encounter(encounter_id: str, encounter: EncounterUpdateModel):
    logger.info(f"Updating encounter ID:{encounter_id}")
    return EncounterClient.update_by_patient_id(encounter_id, encounter)


@router.delete("/encounter/{encounter_id}")
@permission_required("ENCOUNTER", "DELETE")
async def delete_encounter(encounter_id: str):
    logger.info(f"Deleting encounter ID:{encounter_id}")
    return EncounterClient.delete_by_patient_id(encounter_id)
