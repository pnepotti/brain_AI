from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .patient import PatientResponse 
from .user import UserResponse
from .prediction import PredictionResponse

class AnalysisBase(BaseModel):
    patient_id: Optional[int] = None

class AnalysisCreate(AnalysisBase):
    image_path: str
    prediction: Optional[PredictionResponse] = None

class AnalysisUpdate(BaseModel):
    patient_id: Optional[int] = None

class AnalysisDoctorUpdate(BaseModel):
    doctor_diagnosis: str
    is_verified: bool = True

class AnalysisResponse(AnalysisBase):
    id: int
    image_path: str
    
    is_verified: bool
    doctor_diagnosis: Optional[str] = None
    verified_at: Optional[datetime] = None
    
    uploader_id: int
    validator_id: Optional[int] = None

    patient: Optional[PatientResponse] = None
    uploader: Optional[UserResponse] = None
    validator: Optional[UserResponse] = None
    prediction: Optional[PredictionResponse] = None
    
    class Config:
        from_attributes = True