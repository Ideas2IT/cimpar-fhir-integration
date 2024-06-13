from pydantic import BaseModel


class MedicationListModel(BaseModel):
    medication_name : str