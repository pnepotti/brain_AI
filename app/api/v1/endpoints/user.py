from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse, UserUpdate, UserCreate, UserUpdateMe
from app.api.deps import get_db, require_role, get_current_user 
from app.services.user_service import user_service
from app.models.user import UserRole

router = APIRouter()

@router.get("/")
async def get_user_info(current_user: UserResponse = Depends(require_role(UserRole.ADMIN))):
    return {"message": "User information"}

@router.get("/me", response_model=UserResponse)
async def get_own_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_current_user(data: UserUpdateMe, current_user: UserResponse = Depends(get_current_user)):
    return await user_service.update_current_user(current_user.id, data)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(require_role(UserRole.ADMIN))):
    try:
        return await user_service.create_user(db=db, user_in=data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, current_user: UserResponse = Depends(require_role(UserRole.ADMIN))):
    return await user_service.delete_user(user_id=id)

@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(id: int, data: UserUpdate, current_user: UserResponse = Depends(require_role(UserRole.ADMIN))):
    return await user_service.update_user(user_id=id, user_in=data)
