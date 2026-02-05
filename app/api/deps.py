from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security_utils import verify_token
from app.core.exceptions import UnauthorizedError
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obtener sesión de BD.
    
    Yield:
        AsyncSession: Sesión de BD asíncrona
    """
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency para obtener el usuario actual desde el JWT token.
    
    Valida el token JWT en el header Authorization: Bearer <token>
    Decodifica el token y busca el usuario en BD.
    
    Args:
        credentials: Credenciales HTTP (token JWT)
        db: Sesión de BD asíncrona
        
    Returns:
        User: Usuario actual si el token es válido
        
    Raises:
        HTTPException 401: Si el token es inválido, expirado o no existe
    """
    token = credentials.credentials
    
    try:
        # 1. Validar y decodificar el token
        payload = verify_token(token)
        
        # 2. Extraer el user_id del payload
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token sin 'sub' claim")
            raise UnauthorizedError("Token inválido")
        
        # 3. Convertir a int
        try:
            user_id = int(user_id)
        except ValueError:
            logger.warning(f"User ID inválido en token: {user_id}")
            raise UnauthorizedError("Token inválido")
        
        # 4. Buscar usuario en BD
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()
        
        if user is None:
            logger.warning(f"Usuario con ID {user_id} no encontrado")
            raise UnauthorizedError("Usuario no encontrado")
        
        # 5. Verificar que el usuario esté activo
        if not user.is_active:
            logger.warning(f"Intento de acceso con usuario inactivo: {user.email}")
            raise UnauthorizedError("Usuario inactivo")
        
        logger.debug(f"Usuario autenticado: {user.email}")
        return user
        
    except JWTError as e:
        logger.warning(f"Error validando token JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Error inesperado en get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error validando token",
            headers={"WWW-Authenticate": "Bearer"},
        )