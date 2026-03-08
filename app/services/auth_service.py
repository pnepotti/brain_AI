from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security_utils import verify_password, create_access_token
from app.core.exceptions import (
    InvalidCredentialsError,
    InactiveUserError,
    UserNotFoundError
)
from app.repositories.user_repository import user_repository
from app.schemas.auth import LoginRequest,TokenResponse
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Servicio para autenticación y generación de tokens."""
    
    async def login(self, db: AsyncSession, login_in: LoginRequest, token_expire_minutes: int = 30) -> TokenResponse:
        """Autentica un usuario y genera JWT token."""
        
        user = await user_repository.get_by_email(db, login_in.email)
            
        if not user:
            logger.warning(f"Login attempt con email no registrado: {login_in.email}")
            raise UserNotFoundError(f"No existe usuario con email: {login_in.email}")
            
        if not verify_password(login_in.password, user.password_hash):
            logger.warning(f"Failed login attempt para usuario: {login_in.email}")
            raise InvalidCredentialsError("Contraseña incorrecta")
            
        if not user.is_active:
            logger.warning(f"Login attempt de usuario inactivo: {login_in.email}")
            raise InactiveUserError(f"Usuario {login_in.email} está inactivo")
            
        access_token_expires = timedelta(minutes=token_expire_minutes)
        access_token = create_access_token(
            data={
                "sub": str(user.id), 
                "email": user.email,
                "role": user.role
            },
            expires_delta=access_token_expires
        )
            
        logger.info(f"Login exitoso para usuario: {login_in.email}")
            
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=token_expire_minutes * 60  # segundos
        )
        

    async def logout(self, user_id: int):
        """Logout (en JWT stateless no se requiere BD)."""

        logger.info(f"Logout para usuario ID: {user_id}")
        # El frontend elimina el token localmente.
        return {"message": "Logout exitoso"}

    async def refresh_token(self, db: AsyncSession, user_id: int, token_expire_minutes: int = 30) -> TokenResponse:
        """Refresca el JWT token de un usuario."""

        user = await user_repository.get_by_id(db, user_id)
                
        if not user:
            raise UserNotFoundError(f"Usuario con ID {user_id} no existe")
        
        if not user.is_active:
            raise InactiveUserError(f"Usuario está inactivo")
        
        # Generar nuevo token
        access_token_expires = timedelta(minutes=token_expire_minutes)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            },
            expires_delta=access_token_expires
        )
        
        logger.info(f"Token refrescado para usuario ID: {user_id}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=token_expire_minutes * 60
        )


# Crear instancia única para usar en toda la app
auth_service = AuthService()