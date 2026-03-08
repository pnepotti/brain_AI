from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.patient_repository import patient_repository
from app.models.patient import Patient
from app.core.exceptions import PatientNotFoundError
import logging

logger = logging.getLogger(__name__)

class PatientService:
    async def get_patient(self, db: AsyncSession, patient_id: int) -> Patient:
        """Obtener paciente por ID."""
        patient = await patient_repository.get_by_id(db, patient_id)
        if not patient:
            raise PatientNotFoundError(f"Paciente con ID {patient_id} no encontrado")
        return patient
    
    async def create_patient(self, db: AsyncSession, patient_in: Patient) -> Patient:
        """Crear un nuevo paciente."""
        existing_patient = await patient_repository.get_by_id(db, patient_in.id)
        if existing_patient:
            raise PatientNotFoundError(f"Paciente con ID {patient_in.id} ya existe")
        created_patient = await patient_repository.create(db, patient_in)
        logger.info(f"Paciente creado: ID {patient_in.id}")
        return created_patient
    
    async def update_patient(self, db: AsyncSession, patient_id: int, **kwargs) -> Patient:
        """Actualizar un paciente."""
        patient = await patient_repository.get_by_id(db, patient_id)
        if not patient:
            raise PatientNotFoundError(f"Paciente con ID {patient_id} no encontrado")
        updated_patient = await patient_repository.update_by_id(db, patient_id, **kwargs)
        logger.info(f"Paciente actualizado: ID {patient_id}")
        return updated_patient
    
    async def delete_patient(self, db: AsyncSession, patient_id: int) -> Patient:
        """Eliminar un paciente."""
        patient = await patient_repository.delete_by_id(db, patient_id)
        if not patient:
            raise PatientNotFoundError(f"Paciente con ID {patient_id} no encontrado")
        logger.info(f"Paciente eliminado: ID {patient_id}")
        return patient
    
patient_service = PatientService()