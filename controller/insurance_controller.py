from fastapi import Response, status
import logging
import traceback

from aidbox.base import Reference, CodeableConcept, Coding
from aidbox.resource.coverage import Coverage_Class

from constants import GROUP_SYSTEM, GROUP_CODE,PATIENT_REFERENCE
from services.aidbox_resource_wrapper import Coverage 
from models.insurance_validation import CoverageModel, CoverageUpdateModel

logger = logging.getLogger("log")


class CoverageClient:
    @staticmethod
    def create_coverage(coverage: CoverageModel):
        try:
            response_coverage = Coverage.make_request(method="GET", endpoint=f"/fhir/Coverage/?beneficiary=Patient/{coverage.beneficiary_id}")
            existing_coverages = response_coverage.json() if response_coverage else {}

            patient_id_occurrences = sum(1 for entry in existing_coverages.get('entry', []) if entry['resource']['beneficiary']['reference'] == f"Patient/{coverage.beneficiary_id}")

            if patient_id_occurrences >= 3:
                logger.error(f"A patient can only have 3 insurance")
                return Response(
                    content="A patient can only have 3 insurance", status_code=status.HTTP_400_BAD_REQUEST
                )

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
                order=coverage.insurance_type
            )
            insurance_plan.save()
            response_data = {"id": insurance_plan.id, "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Unable to create a insurance_plan: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to Creating Insurance", status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def get_coverage_by_patient_id(patient_id: str):
        try:
            response_coverage = Coverage.make_request(method = "GET", endpoint= f"/fhir/Coverage/?beneficiary=Patient/{patient_id}")

            if not response_coverage:
                return Response(status_code=404, content="Coverage not found")
            coverage = response_coverage.json() 

            return {"coverage": coverage}
        except Exception as e:
            logger.error(f"Unable to get coverage data: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: No Coverage data found for the {patient_id}", status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def update_by_patient_id(patient_id: str, insurance_id: str,updated_coverage: CoverageUpdateModel):
        try:

            insurance_plan = Coverage(
                id=insurance_id,
                status=updated_coverage.status,
                beneficiary=Reference(reference=f"{PATIENT_REFERENCE}/{patient_id}"),
                subscriberId=updated_coverage.policy_number,
                payor=[Reference(display=updated_coverage.provider_name)],
                class_=[
                    Coverage_Class(
                    type=CodeableConcept(coding=[Coding(system=GROUP_SYSTEM, code=GROUP_CODE)]),
                    value=updated_coverage.group_number,
                )],
                order=updated_coverage.insurance_type
            )
            insurance_plan.save()
            response_data = {"id": insurance_plan.id, "updated": True}
            logger.info(f"Added Updated in DB: {response_data}")
            return response_data

        except Exception as e:
            logger.error(f"Unable to update coverage data: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to update coverage data for the {patient_id}", status_code=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def delete_by_patient_id(patient_id: str):
        try:
            response_coverage = Coverage.make_request(method = "DELETE", endpoint= f"/fhir/Coverage/?beneficiary=Patient/{patient_id}")
            return {"deleted": True, "patient_id": patient_id}
        except Exception as e:
            logger.error(f"Unable to delete coverage data: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to delete coverage data for the {patient_id}", status_code=status.HTTP_400_BAD_REQUEST
            )

