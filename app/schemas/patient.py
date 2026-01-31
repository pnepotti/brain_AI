from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    identifier: str # DNI
    full_name: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    identifier: Optional[str] = None
    full_name: Optional[str] = None

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True