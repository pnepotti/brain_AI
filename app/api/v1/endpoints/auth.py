# app/api/v1/endpoints/auth.py (actualizado)
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.auth_service import auth_service
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.exceptions import (
    InvalidCredentialsError,
    InactiveUserError,
    UserNotFoundError,
    AppException
)

router = APIRouter()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para login.
    
    Returns:
        - 200: Token JWT generado exitosamente
        - 401: Credenciales inválidas o usuario inactivo
        - 404: Usuario no encontrado
    """
    try:
        token = await auth_service.login(
            db=db,
            email=credentials.email,
            password=credentials.password
        )
        return token
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error durante login"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Endpoint para logout.
    
    En JWT stateless, el cliente elimina el token localmente.
    El backend solo confirma el logout.
    """
    result = await auth_service.logout(user_id=None)  # user_id vendría del JWT
    return result


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)  # Necesitas implementar esto
):
    """
    Endpoint para refrescar el JWT token.
    
    Requiere autenticación previa (token válido).
    """
    try:
        token = await auth_service.refresh_token(
            db=db,
            user_id=current_user_id
        )
        return token
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)