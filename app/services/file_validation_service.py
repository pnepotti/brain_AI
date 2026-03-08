from fastapi import UploadFile
from app.core.exceptions import InvalidImageError
import logging

logger = logging.getLogger(__name__)

class FileValidationService:
    """Servicio para validar el archivo de imagen subido."""
    
    def __init__(self):
        pass

    async def validate(self, file_content: bytes, file: UploadFile) -> bool:
        
        if len(file_content) == 0:
            raise InvalidImageError("El archivo está vacío")
        
        if not file.content_type or not file.content_type.startswith("image/"):
            logger.warning(f"Intento de subir archivo no-imagen: {file.content_type}")
            raise InvalidImageError(f"Formato no válido. Se requiere imagen. Recibido: {file.content_type}")
        
        # VALIDACION DE IMAGEN MRI
        # Aquí iría la lógica específica para validar imágenes MRI
        
        return True

# Instancia Singleton para usar en otros servicios (Inyección de Dependencias)
file_validation_service = FileValidationService()