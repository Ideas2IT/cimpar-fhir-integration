import logging

from models.patient_validation import PatientModel
from controller.patient_controller import PatientClient

logger = logging.getLogger("log")


class PatientService:
    @staticmethod
    def create_patient(pat: PatientModel):
        logger.info(f"Payload:{pat}")
        response = PatientClient.create(pat)
        logger.info(f"Response:{pat}")
        return response
    
    @staticmethod
    def get_patient_by_id(patient_id: str):
        logger.info(f"Patient ID:{patient_id}")
        return PatientClient.get_patient_by_id(patient_id)
    
    @staticmethod
    def get_all_patients():
        logger.info("Fetching all patients")
        return PatientClient.get_all_patients()
    
    @staticmethod
    def delete_patient_by_id(patient_id: str):
        logger.info(f"Deleting patient ID:{patient_id}")
        return PatientClient.delete_patient_by_id(patient_id)
        