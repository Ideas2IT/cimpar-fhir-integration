import logging

from controller.hl7_immunization_controller import HL7ImmunizationClient

logger = logging.getLogger("log")


class HL7ImmunizationService:

    @staticmethod
    def create_vx04(vx04_data):
        logger.info("Payload: %s" % vx04_data)
        response = HL7ImmunizationClient().create(vx04_data)
        logger.info("Response: %s" % response)
        return response

