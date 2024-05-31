import logging

from models.medication_validation import MedicationCreateModel, MedicationUpdateModel
from controller.medication_controller import MedicationClient

logger = logging.getLogger("log")


class MedicationService:
    @staticmethod
    def create_medication(med: MedicationCreateModel):
        logger.info(f"Payload:{med}")
        response = MedicationClient.create_medication(med)
        logger.info(f"Response:{med}")
        return response
    
    @staticmethod
    def get_medication_by_patient_id(patient_id: str):
        logger.info(f"Patient ID:{patient_id}")
        response = MedicationClient.get_medication_by_patient_id(patient_id)
        logger.info(f"Response:{response}")
        return response
    
    @staticmethod
    def update_medication_by_patient_id(patient_id: str, updated_medication: MedicationUpdateModel):
        logger.info(f"Updating medication for patient ID:{patient_id} with data:{updated_medication}")
        response = MedicationClient.update_medication_by_patient_id(patient_id, updated_medication)
        logger.info(f"Response:{response}")
        return response

