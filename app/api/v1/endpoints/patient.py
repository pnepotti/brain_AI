from fastapi import APIRouter, status, Depends
from app.schemas.patient import PatientCreate, PatientUpdate
from app.models.user import UserRole
from app.schemas.user import UserResponse
from app.api.deps import get_db, require_role, get_current_user

router = APIRouter()

@router.get("/")
async def get_patient_info(current_user: UserResponse = Depends(require_role([UserRole.ADMIN, UserRole.DOCTOR]))):
    return {"message": "Patient information"}

@router.post("/", response_model=PatientCreate, status_code=status.HTTP_201_CREATED)
async def create_patient(data: PatientCreate, current_user: UserResponse = Depends(require_role([UserRole.ADMIN, UserRole.DOCTOR]))):
    return {"message": "Patient created", "data": data}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(id: int, current_user: UserResponse = Depends(require_role([UserRole.ADMIN, UserRole.DOCTOR]))):
    pass

@router.patch("/{id}", response_model=PatientUpdate, status_code=status.HTTP_200_OK)
async def update_patient(id: int, data: PatientUpdate, current_user: UserResponse = Depends(require_role([UserRole.ADMIN, UserRole.DOCTOR]))):
    return {"message": f"Patient with id {id} updated", "data": data}   
