from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse, UserUpdate, UserCreate, UserUpdateMe
from app.core.deps import get_db, require_role, get_current_user 
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
async def update_current_user(
    data: UserUpdateMe, 
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    return await user_service.update_current_user(db=db, user_id=current_user.id, user_in=data)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: UserResponse = Depends(require_role(UserRole.ADMIN))
):
    """
    Crear nuevo usuario (solo admin).
    Las excepciones se capturan automáticamente por el handler global.
    """
    return await user_service.create_user(db=db, user_in=data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_role(UserRole.ADMIN))
):
    return await user_service.delete_user(db=db, user_id=id)

@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    id: int, 
    data: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_role(UserRole.ADMIN))
):
    return await user_service.update_user(db=db, user_id=id, user_in=data)
