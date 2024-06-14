"""
Created the Separate aidbox resources which is wrapper for already existing resources.
To support the Bearer token authentication for each API request for all the API calls.
"""
from services.aidbox_service import AidboxApi
from aidbox.resource.patient import Patient as PatientR


class Patient(AidboxApi, PatientR):
    pass

