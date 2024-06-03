import logging
import traceback
from fastapi import Response, status

from aidbox.base import Period,  CodeableConcept, Reference, Coding
from aidbox.resource.encounter import Encounter, Encounter_Participant, Encounter_Location
from models.encounter_validation import EncounterModel

logger = logging.getLogger("log")


class EncounterClient:
    @staticmethod
    def create(enc: EncounterModel):
        try:
            encounter = Encounter(
                status=enc.status,
                class_=Coding(code=enc.class_, display="inpatient encounter"),
                period=Period(start=enc.admission_date, end=enc.discharge_date),
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
                content=response_data, status_code=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_encounter_by_id(encounter_id: str):
        try:
            encounter = Encounter.from_id(encounter_id)
            if encounter:
                logger.info(f"Encounter Found: {encounter_id}")
                return encounter
            return Response(
                content={"Error retrieving encounters"}, status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving encounters: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content={"Error retrieving encounters"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def delete_encounter(encounter_id: str):
        try:
            encounter = Encounter(id=encounter_id)
            encounter.delete()
            return {"deleted": True}
        except Exception as e:
            logger.error(f"Unable to delete encounter: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content={"error": "Unable to delete encounter"}, status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod   
    def get_all_encounters():
        try:
            encounters = Encounter.get()
            if encounters:
                logger.info(f"Encounters Found: {len(encounters)}")
                return encounters
            return Response(content={"Encounters not found"}, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving encounters: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content={"Error retrieving encounters"}, status_code=status.HTTP_400_BAD_REQUEST
            )
