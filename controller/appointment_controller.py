import logging
import traceback
from fastapi import status
from fastapi.responses import JSONResponse

from aidbox.base import CodeableConcept, Reference, Coding
from aidbox.resource.appointment import Appointment_Participant

from constants import PATIENT_REFERENCE, INTEND, STATUS
from services.aidbox_resource_wrapper import Appointment
from models.appointment_validation import AppoinmentModel
from services.aidbox_resource_wrapper import MedicationRequest
from services.aidbox_resource_wrapper import AllergyIntolerance
from services.aidbox_resource_wrapper import MedicationStatement


logger = logging.getLogger("log")


class AppointmentClient:
    @staticmethod
    def create_appointment(patient_id: str, app: AppoinmentModel):
        try:
            appointment = Appointment(
                status=app.status,
                description=app.other_reason,
                reasonCode=[CodeableConcept(coding=[Coding(display=app.test_to_take)])],
                participant=[
                    Appointment_Participant(
                        actor=Reference(reference=f"{PATIENT_REFERENCE}/{patient_id}"),
                        status=app.participant_status,
                    )
                ],
                start=app.date_of_appoinment,
                end=app.schedule_time,
                patientInstruction=app.reason_for_test,
            )
            appointment.save()

            if app.current_medication and any(
                item.display
                for item in app.current_medication
                if hasattr(item, "display")
            ):
                medication_statement = MedicationStatement(
                    status=STATUS,
                    medicationCodeableConcept=CodeableConcept(
                        coding=[
                            Coding(
                                system=concept.system,
                                code=concept.code,
                                display=concept.display,
                            )
                            for concept in app.current_medication
                        ]
                    ),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{patient_id}"),
                )
                medication_statement.save()

            if app.other_medication and any(
                hasattr(concept, "display") and concept.display
                for concept in app.other_medication
            ):
                medication_request = MedicationRequest(
                    medicationCodeableConcept=CodeableConcept(
                        coding=[
                            Coding(
                                system=concept.system,
                                code=concept.code,
                                display=concept.display,
                            )
                            for concept in app.other_medication
                        ]
                    ),
                    subject=Reference(reference=f"{PATIENT_REFERENCE}/{patient_id}"),
                    status=STATUS,
                    intent=INTEND,
                )
                medication_request.save()

            if app.current_allergy and any(
                hasattr(concept, "display") and concept.display
                for concept in app.current_allergy
            ):
                current_allergy = AllergyIntolerance(
                    code=CodeableConcept(
                        coding=[
                            Coding(
                                system=concept.system,
                                code=concept.code,
                                display=concept.display,
                            )
                            for concept in app.current_allergy
                        ]
                    ),
                    patient=Reference(reference=f"{PATIENT_REFERENCE}/{patient_id}"),
                )
                current_allergy.save()

            response_data = {
                "appointment_id": appointment.id,
                "current_medication_id": medication_statement.id
                if medication_statement
                else None,
                "other_medication_id": medication_request.id
                if medication_request
                else None,
                "current_allergy": current_allergy.id if current_allergy else None,
                "created": True,
            }
            logger.info(f"Added Successfully in DB: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Error creating Appointment {str(e)}")
            logger.error(traceback.format_exc())
            error_response_data = {
                "error": "Unable to create Appointment",
                "details": str(e),
            }

            return JSONResponse(
                content=error_response_data, status_code=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_all_appointment():
        try:
            appointment = Appointment.get()
            if appointment:
                return appointment
            return JSONResponse(
                content={"Error retrieving appointments"}, status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving encounters: {str(e)}")
            logger.error(traceback.format_exc())
            error_response_data = {
                "error": "Unable to retrieve appointments",
                "details": str(e),
            }

            return JSONResponse(
                content=error_response_data,
                status_code=status.HTTP_400_BAD_REQUEST
            )

