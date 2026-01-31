from fastapi import APIRouter, status

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
async def login():
    return {"message": "Login successful"}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    return {"message": "Logout successful"}