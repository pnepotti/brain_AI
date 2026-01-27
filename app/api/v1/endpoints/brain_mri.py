from fastapi import APIRouter

router = APIRouter()

@router.get("/brain-mri")
async def get_brain_mri_info():
    return {"message": "Brain MRI information"}

@router.post("/brain-mri/upload")
async def upload_brain_mri(data: dict):
    return {"message": "Brain MRI uploaded", "data": data}

@router.delete("/brain-mri/{mri_id}")
async def delete_brain_mri(mri_id: int):
    return {"message": f"Brain MRI with id {mri_id} deleted"}

@router.put("/brain-mri/{mri_id}")
async def update_brain_mri(mri_id: int, data: dict):
    return {"message": f"Brain MRI with id {mri_id} updated", "data": data}




