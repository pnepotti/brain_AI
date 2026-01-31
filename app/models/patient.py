from sqlalchemy import Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=True)
    identifier = Column(String, nullable=False, unique=True)  # e.g., medical record number or DNI

    analyses = relationship("Analysis", back_populates="patient")