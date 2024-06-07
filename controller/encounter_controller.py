import logging
import traceback
from fastapi import Response, status

from aidbox.base import API
from aidbox.base import Period,  CodeableConcept, Reference, Coding
from aidbox.resource.encounter import Encounter, Encounter_Participant, Encounter_Location

from constants import PATIENT_REFERENCE, CLASS_DISPLAY
from models.encounter_validation import EncounterModel, EncounterUpdateModel

logger = logging.getLogger("log")


class EncounterClient:
    @staticmethod
    def create_encounter(enc: EncounterModel):
        try:
            encounter = Encounter(
                status=enc.status,
                class_=Coding(code=enc.class_code, display=CLASS_DISPLAY),
                period=Period(start=enc.admission_date, end=enc.discharge_date),
                subject=Reference(reference=f"{PATIENT_REFERENCE}/{enc.patient_id}"),
                reasonCode=[CodeableConcept(text=enc.reason)],
                participant=[Encounter_Participant(individual=Reference(display=enc.primary_care_team))], 
                location=[Encounter_Location(location=Reference(display=enc.location))],
            )
            encounter.save()
            response_data = {"id": encounter.id, "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Error creating encounters {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to Creating Encounter", status_code=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_encounter_by_id(patient_id: str):
        try:
            encounter = API.do_request(method = "GET", endpoint= f"/fhir/Encounter/?subject=Patient/{patient_id}")
            if encounter:
                logger.info(f"Encounter Found: {patient_id}")
                return encounter.json()
            return Response(
                content={"Error retrieving encounters for {patient_id}"}, status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving encounters: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to get encounter", status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def update_by_patient_id(patient_id: str , enc: EncounterUpdateModel):
        try:
            encounter = Encounter(
                id=enc.id,
                status=enc.status,
                class_=Coding(code=enc.class_code, display=CLASS_DISPLAY),
                period=Period(start=enc.admission_date, end=enc.discharge_date),
                subject=Reference(reference=f"{PATIENT_REFERENCE}/{enc.patient_id}"),
                reasonCode=[CodeableConcept(text=enc.reason)],
                participant=[Encounter_Participant(individual=Reference(display=enc.primary_care_team))], 
                location=[Encounter_Location(location=Reference(display=enc.location))],
            )
            encounter.save()
            logger.info(f"Updated Successfully in DB: {patient_id}")
            return {"updated": True, "encounter": encounter.id}
        except Exception as e:
            logger.error(f"Unable to update encounter: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to update encounter", status_code=status.HTTP_400_BAD_REQUEST
            )
    
    @staticmethod
    def get_all_encounters():
        try:
            encounters = API.do_request(method = "GET", endpoint= f"/fhir/Encounter")
            if encounters:
                logger.info(f"Encounters Found")
                return encounters.json()
            return Response(
                content={"Error retrieving encounters"}, status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving encounters: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to get encounters", status_code=status.HTTP_400_BAD_REQUEST
            )


    @staticmethod
    def delete_by_patient_id(patient_id: str):
        try:
            encounter = API.do_request(method = "DELETE", endpoint= f"/fhir/Encounter/?subject=Patient/{patient_id}")
            return {"deleted": True, "encounter": encounter.id}
        except Exception as e:
            logger.error(f"Unable to delete encounter: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to delete encounter", status_code=status.HTTP_400_BAD_REQUEST
            )
        



