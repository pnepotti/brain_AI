from sqlalchemy.future import select
from app.models.user import User
from .security_utils import verify_password, create_access_token
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import user_repository
from app.core.exceptions import UserNotFoundError, InactiveUserError, InvalidCredentialsError
from app.schemas.auth import TokenResponse
import logging

logger = logging.getLogger(__name__)

async def login_service(db: AsyncSession, email: str, password: str):
    """Lógica de negocio para login."""

    user = await user_repository.get_by_email(db, email)

    if not user:
        raise UserNotFoundError(f"Usuario con email {email} no encontrado")
    
    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Credenciales inválidas")
        
    if not user.is_active:
        raise InactiveUserError("Usuario inactivo")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Login exitoso para usuario: {email}")

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.total_seconds()
    )




async def logout_service():
    # En JWT stateless, el backend no necesita borrar nada.
    # Simplemente se responde OK para que el frontend proceda a borrar el token localmente.
    logger.info("Logout exitoso.")
    return {"message": "Logout exitoso. Por favor elimine el token del cliente."}
