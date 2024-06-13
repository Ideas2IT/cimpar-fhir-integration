import logging
import traceback
import logging
from fastapi import Response, status

from aidbox.base import API

logger = logging.getLogger("log")


class MedicationList:
    @staticmethod
    def get_medication_list(medication_name: str):
        try:
            medication_list_snomed = API.make_request(
                method="GET",
                endpoint=f"/Concept?.display$contains={medication_name}&.system=http://snomed.info/sct",
            )
            logger.info(f"Medication List: {medication_list_snomed}")
            if not medication_list_snomed:
                return Response(status_code=404, content="Medication not found")
            return {
                "medication_list": medication_list_snomed.json()
            }
        except Exception as e:
            logger.error(f"Unable to get medication list: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: No Medication data found for the {medication_name}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
    @staticmethod
    def get_allergy_list(allergy_name: str):
        try:
            allergy_list = API.make_request(
                method="GET",
                endpoint=f"/Concept?.definition$contains={allergy_name}&system=http://hl7.org/fhir/sid/icd-10",
            )
            logger.info(f"Allergy List: {allergy_list}")
            if not allergy_list:
                return Response(status_code=404, content="Allergy not found")
            return {
                "allergy_list": allergy_list.json()
            }
        except Exception as e:
            logger.error(f"Unable to get allergy list: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: No Allergy data found for the {allergy_name}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
