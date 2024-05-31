import logging

from models.encounter_validation import EncounterModel
from controller.encounter_controller import EncounterClient

logger = logging.getLogger("log")


class EncounterService:
    @staticmethod
    def create_encounter(enc: EncounterModel):
        logger.info(f"Payload:{enc}")
        response = EncounterClient.create(enc)
        logger.info(f"Response:{response}")
        return response

    @staticmethod
    def get_encounter_by_id(encounter_id: str):
        logger.info(f"Encounter ID:{encounter_id}")
        return EncounterClient.get_encounter_by_id(encounter_id)

    @staticmethod
    def get_all_encounters():
        logger.info("Fetching all encounters")
        return EncounterClient.get_all_encounters()

    @staticmethod
    def delete_encounter_by_id(encounter_id: str):
        logger.info(f"Deleting encounter ID:{encounter_id}")
        return EncounterClient.delete_encounter_by_id(encounter_id)