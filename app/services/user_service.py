import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdateMe, UserUpdate
from app.core.security_utils import get_password_hash
from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    ForbiddenError
)
from app.repositories.user_repository import user_repository

logger = logging.getLogger(__name__)


class UserService:
    """Lógica de negocio para usuarios."""

    async def get_user(self, db: AsyncSession, user_id: int) -> User:
        """Obtiene un usuario por ID."""
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(f"Usuario ID {user_id} no existe")
        return user

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Crea un nuevo usuario."""
        # 1. VALIDACIÓN: ¿Email existe?
        existing_user = await user_repository.get_by_email(db, user_in.email)
        
        if existing_user:
            logger.warning(f"Email duplicado: {user_in.email}")
            raise UserAlreadyExistsError(f"Email {user_in.email} ya registrado")
        
        # 2. LÓGICA: Hashear contraseña
        hashed_password = get_password_hash(user_in.password)
        
        # 3. CREAR entidad
        db_user = User(
            email=user_in.email,
            password_hash=hashed_password,
            full_name=user_in.full_name,
            is_active=True,
            role="user"
        )
        
        # 4. GUARDAR en BD (repository se encarga del commit)
        created_user = await user_repository.create(db, db_user)
        logger.info(f"Usuario creado: {user_in.email}")
        return created_user
    
    async def update_user(self, db: AsyncSession, user_id: int, user_in: UserUpdate, current_user: User) -> User:
        """Actualiza un usuario (admin)."""
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(f"Usuario ID {user_id} no existe")
        
        if current_user.role != "admin":
            raise ForbiddenError("Solo admin puede editar usuarios")
        
        update_data = user_in.model_dump(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        if "email" in update_data and update_data["email"] != user.email:
            existing = await user_repository.get_by_email(db, update_data["email"])
            if existing:
                raise UserAlreadyExistsError(f"Email {update_data['email']} ya existe")
        
        updated_user = await user_repository.update_by_id(db, user_id, **update_data)
        
        logger.info(f"Usuario actualizado: ID {user_id}")
        return updated_user
    
    async def update_current_user(self, db: AsyncSession, user_id: int, user_in: UserUpdateMe) -> User:
        """Usuario actualiza su propio perfil."""
        # 1. VALIDACIÓN: ¿Existe?
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(f"Usuario ID {user_id} no existe")
        
        # 2. PREPARAR UPDATE
        update_data = user_in.model_dump(exclude_unset=True)
        
        # 3. LÓGICA: Si cambia contraseña, hashearla
        if "password" in update_data and update_data["password"]:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        # 4. GUARDAR en BD
        updated_user = await user_repository.update_by_id(db, user_id, **update_data)
        
        logger.info(f"Usuario actualizado (self): ID {user_id}")
        return updated_user
    
    async def delete_user(
        self,
        db: AsyncSession,
        user_id: int,
        current_user: User
    ) -> None:
        """
        Elimina un usuario (soft delete - marca como inactivo).
        
        Raises:
            UserNotFoundError: Si el usuario no existe
            ForbiddenError: Si no tiene permiso o intenta auto-eliminarse
        """
        # 1. VALIDACIÓN: ¿Existe?
        user = await user_repository.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundError(f"Usuario ID {user_id} no existe")
        
        # 2. VALIDACIÓN: ¿Tiene permiso?
        if current_user.role != "admin":
            raise ForbiddenError("Solo admin puede eliminar usuarios")
        
        # 3. VALIDACIÓN: ¿No intenta auto-eliminarse?
        if current_user.id == user_id:
            raise ForbiddenError("No puedes eliminarte a ti mismo")
        
        # 4. LÓGICA: Soft delete (marcar como inactivo)
        await user_repository.update_by_id(db, user_id, is_active=False)
        
        logger.warning(f"Usuario eliminado: ID {user_id} por admin: {current_user.id}")


user_service = UserService()