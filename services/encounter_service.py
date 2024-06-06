import logging

from models.encounter_validation import EncounterModel, EncounterUpdateModel
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
    def get_encounter_by_id(patient_id: str):
        logger.info(f"Encounter ID:{patient_id}")
        return EncounterClient.get_encounter_by_id(patient_id)
    
    @staticmethod
    def update_encounter_by_patient_id(patient_id: str, updated_encounter: EncounterUpdateModel):
        logger.info(f"Updating encounter for patient with ID: {patient_id}")
        response = EncounterClient.update_by_patient_id(patient_id, updated_encounter)
        logger.info(f"Response: {response}")
        return response

    
    @staticmethod
    def delete_encounter_by_patient_id(patient_id: str):
        logger.info(f"Deleting encounter for patient with ID: {patient_id}")
        response = EncounterClient.delete_by_patient_id(patient_id)
        logger.info(f"Response: {response}")
        return response
