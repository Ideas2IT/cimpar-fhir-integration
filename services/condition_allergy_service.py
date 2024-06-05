import logging

from models.condition_validation import ConditionModel, ConditionUpdateModel
from controller.condition_allergy_controller import ConditionClient

logger = logging.getLogger("log")


class ConditionAllergyService:
    @staticmethod
    def create_condition_allergy(con: ConditionModel):
        logger.info(f"Payload:{con}")
        response = ConditionClient.create_condition_allergy(con)
        logger.info(f"Response:{response}")
        return response
    
    @staticmethod
    def get_condition_allergy(patient_id: str):
        response = ConditionClient.get_condition_by_patient_id(patient_id)
        logger.info(f"Response:{response}")
        return response
    
    @staticmethod
    def update_condition_allergy(patient_id: str, condition: ConditionUpdateModel):
        logger.info(f"Payload:{condition}")
        response = ConditionClient.update_by_patient_id(patient_id, condition)
        logger.info(f"Response:{response}")
        return response
    
    @staticmethod
    def delete_condition_allergy(patient_id: str):
        response = ConditionClient.delete_condition_by_patient_id(patient_id)
        logger.info(f"Response:{response}")
        return response