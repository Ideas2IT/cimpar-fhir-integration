import logging

from models.insurance_validation import CoverageModel,  CoverageUpdateModel
from controller.insurance_controller import CoverageClient

logger = logging.getLogger("log")


class InsuranceService:
    @staticmethod
    def create_insurance(ins_plan: CoverageModel):
        logger.info(f"Payload:{ins_plan}")
        response = CoverageClient.create(ins_plan)
        logger.info(f"Response:{ins_plan}")
        return response
    
    @staticmethod
    def get_insurance_by_patient_id(patient_id: str):
        return CoverageClient.get_coverage_by_patient_id(patient_id)
    
    @staticmethod
    def update_insurance_by_patient_id(patient_id: str, updated_insurance: CoverageUpdateModel):
        return CoverageClient.update_by_patient_id(patient_id, updated_insurance)

