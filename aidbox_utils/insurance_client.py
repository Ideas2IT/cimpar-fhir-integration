from fastapi import Response, status
import logging
import traceback

from aidbox.resource.insuranceplan import InsurancePlan
from models.insurance_validation import InsuranceModel

logger = logging.getLogger("log")


class InsuranceClient:
    @staticmethod
    def create(ins_plan: InsuranceModel):
        try:
            insurance_plan = InsurancePlan(
                name=ins_plan.name,
                alias=ins_plan.alias
            )
            insurance_plan.save()
            response_data = {"id": insurance_plan.id, "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Unable to create a insurance_plan: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)

