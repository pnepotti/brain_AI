from fastapi import APIRouter
from app.api.v1.endpoints import analysis, patient, user, auth


router = APIRouter()

router.include_router(
    auth.router, prefix="/auth", tags=["auth"]
)
router.include_router(
    analysis.router, prefix="/analyses", tags=["analysis"]
)
router.include_router(
    patient.router, prefix="/patients", tags=["patient"]
)
router.include_router(
    user.router, prefix="/users", tags=["user"]
)