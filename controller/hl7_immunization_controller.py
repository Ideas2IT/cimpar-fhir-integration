from fastapi import Response, status
import logging
import json
import traceback
import requests
from requests.auth import HTTPBasicAuth

from utils.settings import settings
from models.hl7_immunization_validation import VXO4Model

logger = logging.getLogger("log")


class HL7ImmunizationClient:

    def __init__(self):
        self.base_url = settings.AIDBOX_SERVER_URL
        self.token = requests.auth.HTTPBasicAuth(settings.AIDBOX_CLIENT_USERNAME, settings.AIDBOX_CLIENT_PASSWORD)

    def create(self, vx04_content):
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

