import logging

from models.insurance_validation import InsuranceModel
from controller.insurance_controller import InsuranceClient

logger = logging.getLogger("log")


class InsuranceService:
    @staticmethod
    def create_insurance(ins_plan: InsuranceModel):
        logger.info("Payload: %s" % ins_plan)
        response = InsuranceClient.create(ins_plan)
        logger.info("Response: %s" % response)
        return response

