import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate
import time
from typing import Optional
import aiofiles
from app.core.config import settings
from pathlib import Path
from app.models.prediction import Prediction
from app.services.file_validation_service import file_validation_service
from app.services.prediction_service import prediction_service
from app.repositories.analysis_repository import analysis_repository
from app.repositories.prediction_repository import prediction_repository

logger = logging.getLogger(__name__)

class AnalysisService:
    
    async def create_analysis(
        self, 
        db: AsyncSession,
        patient_id: Optional[int],
        file: UploadFile,
        user_id: int
    ) -> Analysis:
        """Crea un nuevo análisis."""
        
        # 1. Lectura y Validación
        file_content = await file.read()
        # validate lanza excepción si falla, no es necesario verificar retorno booleano
        await file_validation_service.validate(file_content, file)
        
        # 2. Guardado de archivo
        upload_dir = Path(settings.UPLOADS_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Manejo seguro si patient_id es None
        safe_patient_id = patient_id if patient_id is not None else "anon"
        filename = f"{safe_patient_id}_{int(time.time())}_{file.filename}"
        file_path = upload_dir / filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)

        # 3. Predicción (IA)
        prediction_data = await prediction_service.predict(str(file_path)) 
        
        # 4. Persistencia en BD
        # Nota: Idealmente esto debería ser una transacción atómica única.
        db_analysis = Analysis(
            patient_id=patient_id,
            image_path=str(file_path),
            uploader_id=user_id
        )
        
        await analysis_repository.create(db, db_analysis)

        db_prediction = Prediction(
            result=prediction_data["prediction"],
            accuracy=prediction_data["accuracy"],
            analysis_id=db_analysis.id  # Vinculación mediante FK
        )

        await prediction_repository.create(db, db_prediction)

        logger.info(f"Análisis creado: id={db_analysis.id}, patient_id={patient_id}")
        return db_analysis
    
    async def delete_analysis(self, db: AsyncSession, analysis_id: int, user_id: int) -> None:
        """Elimina análisis (validar permisos en service)."""
        await analysis_repository.delete_by_id(db, analysis_id)
        logger.info(f"Análisis eliminado: id={analysis_id}")    
    
    async def update_analysis(self, db: AsyncSession, analysis_id: int, data: AnalysisUpdate) -> Analysis:
        """Actualiza análisis."""
        # Por el momento no esta permitido actualizar los datos del analysis
        pass

    async def doctor_diagnosis(self, db: AsyncSession, analysis_id: int, doctor_diagnosis: str) -> Analysis:
        """Permite al doctor agregar su diagnóstico."""
        
        analysis = await analysis_repository.get_by_id(db, analysis_id)
        if not analysis:
            raise ValueError("Análisis no encontrado")
        
        analysis.doctor_diagnosis = doctor_diagnosis
        analysis.is_verified = True
        analysis.verified_at = time.time()  # Timestamp actual
        
        await analysis_repository.update_by_id(db, analysis_id, analysis=analysis)
        logger.info(f"Análisis actualizado con diagnóstico médico: id={analysis_id}")
        return analysis

analysis_service = AnalysisService()