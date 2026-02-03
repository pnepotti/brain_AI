from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse, UserUpdate, UserCreate, UserUpdateMe
from app.api.deps import get_db
from app.services.user_service import user_service

router = APIRouter()

@router.get("/")
async def get_user_info():
    return {"message": "User information"}

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    return {"message": "Current user information"}

@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_current_user(data: UserUpdateMe):
    return {"message": "Current user updated", "data": data}

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.create_user(db=db, user_in=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    pass

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, data: UserUpdate):
    return {"message": f"User with id {user_id} updated", "data": data}
