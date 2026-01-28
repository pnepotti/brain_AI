from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, nullable=False, unique=True)  # e.g., medical record number o DNI
    age = Column(Integer, nullable=False)

    analyses = relationship("Analysis", back_populates="patient")