from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    identifier: str # DNI
    age: int

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    age: Optional[int] = None

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True