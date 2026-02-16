from fastapi import APIRouter, File, UploadFile, Form, status, HTTPException, Depends
from typing import Optional
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate
from app.api.deps import get_db, get_current_user
from app.models.user import UserRole
from app.api.deps import require_role
from app.models.user import User


router = APIRouter()

@router.get("/")
async def get_analysis_info():
    return {"message": "Analysis information"}

@router.post("/", response_model=AnalysisCreate, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    patient_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR))
):
    # Validar que es una imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    return {
        "message": "Analysis created", 
        "filename": file.filename, 
        "patient_id": patient_id # Puede ser None
    }

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(id: int, current_user: User = Depends(require_role(UserRole.ADMIN))):
    pass

@router.patch("/{id}", response_model=AnalysisUpdate, status_code=status.HTTP_200_OK)
async def update_analysis(id: int, data: AnalysisUpdate, current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DOCTOR))):
    return {"message": f"Analysis with id {id} updated", "data": data}
