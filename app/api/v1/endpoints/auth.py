# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db, get_current_user
from app.services.auth_service import auth_service
from app.schemas.auth import LoginRequest, TokenResponse
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    token = await auth_service.login(
        db=db,
        login_in=credentials,
    )
    return token


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: User = Depends(get_current_user)):
    
    result = await auth_service.logout(user_id=current_user.id)
    return result


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    token = await auth_service.refresh_token(
        db=db,
        user_id=current_user.id
    )
    return token