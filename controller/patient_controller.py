import logging
import traceback
from fastapi import Response, status

from aidbox.resource.patient import Patient

from models.patient_validation import PatientModel

logger = logging.getLogger("log")


class PatientClient:
    @staticmethod
    def create(pat: PatientModel):
        try:
            patient = Patient(
            name=[
                {
                    "family": pat.last_name,
                    "given": [pat.first_name, pat.middle_name],
                }
            ],
            gender=pat.gender,
            birthDate=pat.date_of_birth,
            contact=[
                {
                "system": "phone",
                "value": pat.phone_number
                },
                {
                "system": "phone",
                "value": pat.alternate_number
                }
            ],
            address=[
                {
                "country": pat.country,
                "state": pat.state,
                "city": pat.city,
                "postalCode": pat.zip_code,
                "line": [pat.full_address]
                }
            ]
            )
            patient.save()
            response_data = {"id": patient.id, "created": True}
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Unable to create a patient: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content=response_data, status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_patient_by_id(patient_id: str):
        try:
            patient = Patient.from_id(patient_id)
            if patient:
                logger.info(f"Patient Found: {patient_id}")
                return patient
            return Response(content="Patient not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving patient: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content="Error retrieving patient", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def get_all_patients():
        try:
            patients = Patient.get()
            print("patients", patients)
            if patients:
                logger.info(f"Patients Found: {len(patients)}")
                return patients
            return Response(content="Patients not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving patients: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content="Error retrieving patients", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @staticmethod
    def delete_patient_by_id(patient_id: str):
        try:
            patient = Patient(id=patient_id)
            if patient:
                patient.delete()
                return {"message": f"Patient with id {patient_id} has been deleted."}
            return Response(content="Patient not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting patient: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(content="Error deleting patient", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)