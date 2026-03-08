from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prediction import Prediction
from sqlalchemy.future import select

class PredictionRepository:
    async def create(self, db: AsyncSession, prediction: Prediction) -> Prediction:
        db.add(prediction)
        await db.commit()
        await db.refresh(prediction)
        return prediction

    async def get_by_analysis_id(self, db: AsyncSession, analysis_id: int) -> Optional[Prediction]:
        result = await db.execute(select(Prediction).where(Prediction.analysis_id == analysis_id))
        return result.scalars().first()

prediction_repository = PredictionRepository()