from pydantic import BaseModel

class CoverageModel(BaseModel):
    status: str
    beneficiary_id: str
    insurance_type: int
    provider_name: str
    policy_number: str
    group_number: str

class CoverageUpdateModel(BaseModel):
    status: str
    insurance_id: str
    beneficiary_id: str
    insurance_type: int
    provider_name: str
    policy_number: str
    group_number: str

    
