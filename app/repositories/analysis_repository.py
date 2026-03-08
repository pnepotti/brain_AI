from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.analysis import Analysis

class AnalysisRepository:
    async def create(self, db: AsyncSession, analysis: Analysis) -> Analysis:
        db.add(analysis)
        await db.commit()
        await db.refresh(analysis)
        return analysis

    async def get_by_id(self, db: AsyncSession, analysis_id: int) -> Optional[Analysis]:
        result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> List[Analysis]:
        result = await db.execute(select(Analysis))
        return result.scalars().all()
    
    async def update_by_id(self, db: AsyncSession, analysis_id: int, **kwargs) -> Optional[Analysis]:
        analysis = await self.get_by_id(db, analysis_id)
        if not analysis:
            return None
        
        for key, value in kwargs.items():
            if hasattr(analysis, key) and value is not None:
                setattr(analysis, key, value)
        
        db.add(analysis)
        await db.commit()
        await db.refresh(analysis)
        return analysis

    async def delete_by_id(self, db: AsyncSession, analysis_id: int) -> None:
        await db.execute(delete(Analysis).where(Analysis.id == analysis_id))
        await db.commit()

analysis_repository = AnalysisRepository()