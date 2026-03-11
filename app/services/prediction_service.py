import logging

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        """Inicializa el servicio de predicción."""
        
        pass

    def _preprocess_image(self, image_path: str, target_size=(224, 224)):
        """Carga y preprocesa la imagen para el modelo."""
        
        pass

    async def predict(self, image_path: str) -> dict:
        """Realiza la predicción sobre una imagen preprocesada."""
        
        pass
    
prediction_service = PredictionService()