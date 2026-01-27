from fastapi import APIRouter
from app.api.v1.endpoints import brain_mri

router = APIRouter()

router.include_router(
    brain_mri.router, prefix="/brain-mri",tags=["brain-mri"]
)