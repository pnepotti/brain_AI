from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .patient import PatientResponse 
from .user import UserResponse

class AnalysisBase(BaseModel):
    description: Optional[str] = None

# --- INPUTS ---

class AnalysisCreate(AnalysisBase):
    patient_id: int
    image_path: str
    ai_prediction: str
    ai_accuracy: float

class AnalysisDoctorUpdate(BaseModel):
    doctor_diagnosis: str
    is_verified: bool = True

# --- OUTPUTS ---

class AnalysisResponse(AnalysisBase):
    id: int
    image_path: str
    ai_prediction: str
    ai_accuracy: float
    created_at: datetime
    
    is_verified: bool
    doctor_diagnosis: Optional[str] = None
    verified_at: Optional[datetime] = None
    
    patient: Optional[PatientResponse] = None
    uploader: Optional[UserResponse] = None
    validator: Optional[UserResponse] = None

    class Config:
        from_attributes = True