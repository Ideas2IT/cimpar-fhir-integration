from fastapi import Response, status
import logging
import traceback
import requests
from requests.auth import HTTPBasicAuth

from aidbox.base import API
from utils.settings import settings
from models.hl7_immunization_validation import VXO4Model

logger = logging.getLogger("log")


class HL7ImmunizationClient:

    def __init__(self):
        self.base_url = settings.AIDBOX_SERVER_URL
        self.token = requests.auth.HTTPBasicAuth(settings.AIDBOX_CLIENT_USERNAME, settings.AIDBOX_CLIENT_PASSWORD)

    def create_immunization(self, vx04_content):
        try:
            url = self.base_url + "/HL7v2/VXU_V04"
            response_data = requests.post(url, data=vx04_content, auth=self.token)
            logger.info(f"Added Successfully in DB: {response_data}")
            if response_data.status_code == 200:
                return {"status_code": 201, "data": "Record created Successfully"}
            else:
                raise Exception("Unable to create the record")
        except Exception as e:
            logger.error(f"Unable to create a Immunization: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    def get_immunizations_by_patient_id(patient_id: str):
        try:
            response_immunization = API.do_request(method = "GET", endpoint= f"/fhir/Immunization/?patient=Patient/{patient_id}")

            if not response_immunization:
                return Response(status_code=404, content="Immunizations not found")
            immunizations = response_immunization.json() if response_immunization.status_code == 200 else []
            return {"immunizations": immunizations}
        except Exception as e:
            logger.error(f"Unable to get immunization data: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: No Immunization data found for the {patient_id}", status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def get_all_immunizations():
        try:
            response_immunization = API.do_request(method = "GET", endpoint= "/fhir/Immunization")
            if not response_immunization:
                return Response(status_code=404, content="Immunizations not found")
            immunizations = response_immunization.json() 
            return {"immunizations": immunizations}
        except Exception as e:
            logger.error(f"Unable to get immunization data: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content="Error: No Immunization data found", status_code=status.HTTP_400_BAD_REQUEST
            )
        
    
