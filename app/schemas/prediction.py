from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PredictionBase(BaseModel):
    result: str
    accuracy: float

class PredictionCreate(PredictionBase):
    created_at: Optional[datetime] = None
    analysis_id: int

class PredictionResponse(PredictionBase):
    id: int
    analysis_id: int

    class Config:
        from_attributes = True