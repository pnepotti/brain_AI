from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.sql import func

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    image_path = Column(String, nullable=False)
    ai_prediction = Column(String, nullable=False)
    ai_accuracy = Column(Float, nullable=False)  
    result_details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    is_verified = Column(Boolean, default=False)
    doctor_diagnosis = Column(Text, nullable=True) # Corrección o confirmación
    verified_at = Column(DateTime(timezone=True), nullable=True)

    # --- FK ---
    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    patient = relationship("Patient", back_populates="analyses")

    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploader = relationship("User", foreign_keys=[uploader_id], back_populates="uploaded_analyses")

    # C. Quién validó el diagnóstico (Puede ser Null al principio)
    validator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validator = relationship("User", foreign_keys=[validator_id], back_populates="validated_analyses")