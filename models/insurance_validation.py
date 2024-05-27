from pydantic import BaseModel

class CoverageModel(BaseModel):
    status: str
    beneficiary_id: str
    insurance_type: int
    provider_name: str
    policy_number: str
    group_number: str

    
