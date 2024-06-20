import logging
import traceback
from fastapi import Response, status

from aidbox.base import  CodeableConcept, Reference, Coding

from services.aidbox_service import AidboxApi
from constants import PATIENT_REFERENCE, STATUS_SYSTEM
from models.condition_validation import ConditionModel, ConditionUpdateModel
from services.aidbox_resource_wrapper import Condition 
from services.aidbox_resource_wrapper import AllergyIntolerance 

logger = logging.getLogger("log")


class ConditionClient:
    @staticmethod
    def create_condition_allergy(con: ConditionModel):
        try:
            if con.current_condition:
                current_condition = Condition(
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.current_condition]),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                current_condition.save()
            else:
                current_condition = None

            if con.additional_condition and any(concept.display for concept in con.additional_condition):
                additional_condition = Condition(
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.additional_condition]),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                additional_condition.save()
            else:
                additional_condition = None

            if con.current_allergy:
                current_allergy = AllergyIntolerance(
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.current_allergy]),
                    patient=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                current_allergy.save()
            else:
                current_allergy = None

            if con.additional_allergy:
                additional_allergy = AllergyIntolerance(
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.additional_allergy]),
                    patient=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                additional_allergy.save()
            else:
                additional_allergy = None

            if  con.family_condition:
                family_status = "active" if con.family_condition == True else "unknown"
                family_condition = Condition(
                    clinicalStatus=CodeableConcept(coding=[Coding(system=STATUS_SYSTEM, code=family_status)]),
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.family_medications]),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                family_condition.save()

            response_data = {"current_condition": current_condition.id if current_condition else None, 
                             "additional_condition": additional_condition.id if additional_condition else None, 
                             "current_allergy" : current_allergy.id if current_allergy else None, 
                             "additional_allergy" :  additional_allergy.id if additional_allergy else None, 
                             "family_condition" : family_condition.id if family_condition else None,
                             "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Error creating condition: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content="Error: Unable to Creating Condition and Allergy", status_code=status.HTTP_400_BAD_REQUEST
            )
        

    @staticmethod
    def get_condition_by_patient_id(patient_id: str):
        try:
            response_condition = Condition.make_request(method = "GET", endpoint= f"/fhir/Condition/?subject=Patient/{patient_id}")
            response_allergy = AllergyIntolerance.make_request(method = "GET", endpoint= f"/fhir/AllergyIntolerance/?patient=Patient/{patient_id}")

            if not response_condition or not response_allergy:
                return [None, None]
            return [response_condition.json(), response_allergy.json()]
        
        except Exception as e:
            logger.error(f"Error getting condition: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content="Error: Unable to get Condition and Allergy", status_code=status.HTTP_400_BAD_REQUEST
            )
        
    @staticmethod
    def update_by_patient_id(patient_id: str, con: ConditionUpdateModel):
        try:
            if con.current_condition:
                current_condition = Condition(
                    id=con.current_condition_id,
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.current_condition]),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                current_condition.save()
            else:
                current_condition = None

            if con.additional_condition and any(concept.display for concept in con.additional_condition):
                additional_condition = Condition(
                    id=con.additional_condition_id,
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.additional_condition]),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                additional_condition.save()
            else:
                additional_condition = None

            if con.current_allergy:
                current_allergy = AllergyIntolerance(
                    id=con.current_allergy_id,
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.current_allergy]),
                    patient=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                current_allergy.save()
            else:
                current_allergy = None

            if con.additional_allergy:
                additional_allergy = AllergyIntolerance(
                    id=con.additional_allergy_id,
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.additional_allergy]),
                    patient=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                additional_allergy.save()
            else:
                additional_allergy = None

            if  con.family_condition:
                family_status = "active" if con.family_condition == True else "unknown"
                family_condition = Condition(
                    id=con.family_condition_id,
                    clinicalStatus=CodeableConcept(coding=[Coding(system=STATUS_SYSTEM, code=family_status)]),
                    code=CodeableConcept(coding=[Coding(system=concept.system, code=concept.code, display=concept.display) for concept in con.family_medications]),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{con.patient_id}"),
                )
                family_condition.save()

            response_data = {"current_condition": current_condition.id if current_condition else None, 
                             "additional_condition": additional_condition.id if additional_condition else None, 
                             "current_allergy" : current_allergy.id if current_allergy else None, 
                             "additional_allergy" :  additional_allergy.id if additional_allergy else None, 
                             "family_condition" : family_condition.id if family_condition else None,
                             "ptient_id": patient_id,
                             "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Error creating condition: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                content=f"Error: Unable to update Condition and Allergy", status_code=status.HTTP_400_BAD_REQUEST
            )
        

    @staticmethod
    def get_allergy_list(allergy_name: str):
        try:
            allergy_list = AidboxApi.make_request(
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

        