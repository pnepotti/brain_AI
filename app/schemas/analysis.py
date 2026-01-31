from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .patient import PatientResponse 
from .user import UserResponse

class AnalysisBase(BaseModel):
    result_details: Optional[str] = None

class AnalysisCreate(AnalysisBase):
    patient_id: Optional[int] = None
    image_path: str
    ai_prediction: str
    ai_accuracy: float

# Schema para actualizaciones generales (no médicas)
class AnalysisUpdate(BaseModel):
    result_details: Optional[str] = None

class AnalysisDoctorUpdate(BaseModel):
    doctor_diagnosis: str
    is_verified: bool = True

class AnalysisResponse(AnalysisBase):
    id: int
    image_path: str
    ai_prediction: str
    ai_accuracy: float
    created_at: datetime
    
    is_verified: bool
    doctor_diagnosis: Optional[str] = None
    verified_at: Optional[datetime] = None
    
    # IDs explícitos (útiles para referencia rápida en frontend)
    patient_id: Optional[int] = None
    uploader_id: int
    validator_id: Optional[int] = None

    patient: Optional[PatientResponse] = None
    uploader: Optional[UserResponse] = None
    validator: Optional[UserResponse] = None

    class Config:
        from_attributes = True