from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base
from sqlalchemy.orm import relationship
from app.models import analysis  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True) 

    uploaded_analyses = relationship("Analysis", back_populates="uploader", foreign_keys="Analysis.uploader_id")
    validated_analyses = relationship("Analysis", back_populates="validator", foreign_keys="Analysis.validator_id")
