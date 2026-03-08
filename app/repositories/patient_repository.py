from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.patient import Patient
from app.repositories.patient_repository import patient_repository
from sqlalchemy.future import select


class PatientRepository:
    async def get_by_id(self, db: AsyncSession, patient_id: int) -> Optional[Patient]:
        query = select(Patient).where(Patient.id == patient_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def create(self, db: AsyncSession, patient: Patient) -> Patient:
        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        return patient
    
    async def delete_by_id(self, db: AsyncSession, patient_id: int) -> Optional[Patient]:
        patient = await self.get_by_id(db, patient_id)
        if not patient:
            return None
        await db.delete(patient)
        await db.commit()
        return patient
    

    async def update_by_id(self, db: AsyncSession, patient_id: int, **kwargs) -> Optional[Patient]:
        patient = await self.get_by_id(db, patient_id)
        if not patient:
            return None

        for key, value in kwargs.items():
            if hasattr(patient, key) and value is not None:
                setattr(patient, key, value)

        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        return patient

patient_repository = PatientRepository()