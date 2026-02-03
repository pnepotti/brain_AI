from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.security_utils import verify_password, create_access_token
from app.core.exceptions import (
    InvalidCredentialsError,
    InactiveUserError,
    UserNotFoundError
)
from app.schemas.auth import LoginRequest, TokenResponse
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Servicio para autenticación y generación de tokens."""
    
    async def login(
        self, 
        db: AsyncSession, 
        email: str, 
        password: str,
        token_expire_minutes: int = 30
    ) -> TokenResponse:
        """
        Autentica un usuario y genera JWT token.
        
        Args:
            db: Sesión de BD asíncrona
            email: Email del usuario
            password: Contraseña en texto plano
            token_expire_minutes: Minutos hasta expiración del token
            
        Returns:
            TokenResponse con access_token y token_type
            
        Raises:
            UserNotFoundError: Si el usuario no existe
            InvalidCredentialsError: Si la contraseña es incorrecta
            InactiveUserError: Si el usuario está inactivo
        """
        try:
            # 1. Buscar usuario por email
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalars().first()
            
            if not user:
                logger.warning(f"Login attempt con email no registrado: {email}")
                raise UserNotFoundError(f"No existe usuario con email: {email}")
            
            # 2. Verificar contraseña
            if not verify_password(password, user.password_hash):
                logger.warning(f"Failed login attempt para usuario: {email}")
                raise InvalidCredentialsError("Contraseña incorrecta")
            
            # 3. Verificar si el usuario está activo
            if not user.is_active:
                logger.warning(f"Login attempt de usuario inactivo: {email}")
                raise InactiveUserError(f"Usuario {email} está inactivo")
            
            # 4. Crear JWT token
            access_token_expires = timedelta(minutes=token_expire_minutes)
            access_token = create_access_token(
                data={
                    "sub": str(user.id), 
                    "email": user.email,
                    "role": user.role
                },
                expires_delta=access_token_expires
            )
            
            logger.info(f"Login exitoso para usuario: {email}")
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=token_expire_minutes * 60  # segundos
            )
            
        except (UserNotFoundError, InvalidCredentialsError, InactiveUserError):
            raise
        except Exception as e:
            logger.error(f"Error inesperado en login: {str(e)}")
            raise

    async def logout(self, user_id: int):
        """
        Logout (en JWT stateless no se requiere BD).
        
        Args:
            user_id: ID del usuario (para logging)
            
        Returns:
            Mensaje de confirmación
        """
        logger.info(f"Logout para usuario ID: {user_id}")
        # En JWT stateless, el backend no necesita hacer nada en BD.
        # El frontend elimina el token localmente.
        return {"message": "Logout exitoso"}

    async def refresh_token(
        self,
        db: AsyncSession,
        user_id: int,
        token_expire_minutes: int = 30
    ) -> TokenResponse:
        """
        Refresca el JWT token de un usuario.
        
        Args:
            db: Sesión de BD asíncrona
            user_id: ID del usuario
            token_expire_minutes: Minutos hasta expiración del nuevo token
            
        Returns:
            TokenResponse con nuevo access_token
            
        Raises:
            UserNotFoundError: Si el usuario no existe
            InactiveUserError: Si el usuario está inactivo
        """
        # Buscar usuario
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()
        
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