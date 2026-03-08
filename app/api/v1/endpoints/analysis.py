from fastapi import APIRouter, File, UploadFile, Form, status, Depends
from typing import Optional
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate
from app.core.deps import get_db, require_role
from app.models.user import UserRole, User
from app.services.analysis_service import analysis_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/")
async def get_analysis_info(
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db)
):
    return {"message": "Analysis information"}

@router.post("/", response_model=AnalysisCreate, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    patient_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db)
):
    return await analysis_service.create_analysis(
        db=db,
        patient_id=patient_id,
        file=file,
        user_id=current_user.id
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    id: int, 
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    return await analysis_service.delete_analysis(db=db, analysis_id=id, user_id=current_user.id)

@router.patch("/{id}", response_model=AnalysisUpdate, status_code=status.HTTP_200_OK)
async def update_analysis(
    id: int, 
    data: AnalysisUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR)),
    db: AsyncSession = Depends(get_db)
):
    return await analysis_service.update_analysis(db=db, analysis_id=id, data=data)