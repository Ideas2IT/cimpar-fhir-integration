import logging
from fastapi import APIRouter

from models.encounter_validation import EncounterModel
from services.encounter_service import EncounterService

router = APIRouter()
logger = logging.getLogger("log")

@router.post("/encounter")
async def create_encounter(encounter: EncounterModel):
    logger.info(f"Request Payload: {encounter}")
    response = EncounterService.create_encounter(encounter)
    logger.info(f"Response Payload: {response}")
    return response

@router.get("/encounter/{encounter_id}")
async def get_encounter(encounter_id: str):
    logger.info(f"Encounter ID:{encounter_id}")
    return EncounterService.get_encounter_by_id(encounter_id)

@router.get("/encounter")
async def get_all_encounters():
    logger.info("Fetching all encounters")
    return EncounterService.get_all_encounters()

@router.delete("/encounter/{encounter_id}")
async def delete_encounter(encounter_id: str):
    logger.info(f"Deleting encounter ID:{encounter_id}")
    return EncounterService.delete_encounter_by_id(encounter_id)