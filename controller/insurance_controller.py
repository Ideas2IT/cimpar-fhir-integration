from fastapi import Response, status
import logging
import traceback

from aidbox.base import Reference, CodeableConcept, Coding, Extension
from aidbox.resource.coverage import Coverage, Coverage_Class

from constants import GROUP_SYSTEM, GROUP_CODE,PATIENT_REFERENCE, EXTENTION_URL
from models.insurance_validation import CoverageModel

logger = logging.getLogger("log")


class CoverageClient:
    @staticmethod
    def create(coverage: CoverageModel):
        try:
            insurance_plan = Coverage(
                status=coverage.status,
                beneficiary=Reference(reference=f"{PATIENT_REFERENCE}/{coverage.beneficiary_id}"),
                subscriberId=coverage.policy_number,
                payor=[Reference(display=coverage.provider_name)],
                class_=[
                    Coverage_Class(
                    type=CodeableConcept(coding=[Coding(system=GROUP_SYSTEM, code=GROUP_CODE)]),
                    value=coverage.group_number,
                )],
                extension=[Extension(url=EXTENTION_URL, valueInteger=coverage.insurance_type)]
            )
            insurance_plan.save()
            response_data = {"id": insurance_plan.id, "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Unable to create a insurance_plan: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=response_data, status_code=status.HTTP_400_BAD_REQUEST
            )
