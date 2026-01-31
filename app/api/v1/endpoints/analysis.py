from fastapi import APIRouter, File, UploadFile, Form, status, HTTPException
from typing import Optional
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate

router = APIRouter()

@router.get("/")
async def get_analysis_info():
    return {"message": "Analysis information"}

@router.post("/", response_model=AnalysisCreate, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    patient_id: Optional[int] = Form(None),
    file: UploadFile = File(...)
):
    # Validar que es una imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    return {
        "message": "Analysis created", 
        "filename": file.filename, 
        "patient_id": patient_id # Puede ser None
    }

@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(analysis_id: int):
    pass

@router.patch("/{analysis_id}", response_model=AnalysisUpdate, status_code=status.HTTP_200_OK)
async def update_analysis(analysis_id: int, data: AnalysisUpdate):
    return {"message": f"Analysis with id {analysis_id} updated", "data": data}
