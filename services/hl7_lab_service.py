import logging

from controller.hl7_lab_controller import HL7LabClient

logger = logging.getLogger("log")


class HL7LabService:

    @staticmethod
    def create_vx04(vx04_data):
        logger.info("Payload: %s" % vx04_data)
        response = HL7LabClient().create(vx04_data)
        logger.info("Response: %s" % response)
        return response

