from fastapi import APIRouter, status
from app.schemas.patient import PatientCreate, PatientUpdate

router = APIRouter()

@router.get("/")
async def get_patient_info():
    return {"message": "Patient information"}

@router.post("/", response_model=PatientCreate, status_code=status.HTTP_201_CREATED)
async def create_patient(data: PatientCreate):
    return {"message": "Patient created", "data": data}

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int):
    pass

@router.patch("/{patient_id}", response_model=PatientUpdate, status_code=status.HTTP_200_OK)
async def update_patient(patient_id: int, data: PatientUpdate):
    return {"message": f"Patient with id {patient_id} updated", "data": data}   
