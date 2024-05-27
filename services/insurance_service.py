import logging

from models.insurance_validation import CoverageModel
from controller.insurance_controller import CoverageClient

logger = logging.getLogger("log")


class InsuranceService:
    @staticmethod
    def create_insurance(ins_plan: CoverageModel):
        logger.info(f"Payload:{ins_plan}")
        response = CoverageClient.create(ins_plan)
        logger.info(f"Response:{ins_plan}")
        return response

