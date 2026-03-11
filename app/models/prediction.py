from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    result = Column(String, nullable=False)
    probability = Column(Float, nullable=False)   
    entropy = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analysis_id = Column(Integer, ForeignKey("analyses.id"), unique=True, nullable=False)
    analysis = relationship("Analysis", back_populates="prediction")
