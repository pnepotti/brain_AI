from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security_utils import get_password_hash

class UserService:
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        # 1. Verificar si el email ya existe
        query = select(User).where(User.email == user_in.email)
        result = await db.execute(query)
        
        class UserAlreadyExistsError(Exception):
            pass

        if result.scalars().first():
            raise UserAlreadyExistsError(f"Email {user_in.email} ya registrado")

        # 2. Hashear la contraseña
        hashed_password = get_password_hash(user_in.password)

        # 3. Crear instancia del modelo
        db_user = User(
            email=user_in.email,
            password_hash=hashed_password,
            full_name=user_in.full_name,
            is_active=True,
            role="user"
        )
        
        # 4. Guardar en BD
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def update_user(self, user_id: int, user_in: UserCreate) -> User:
        # Implementar lógica de actualización de usuario
        pass

    async def update_current_user(self, user_id: int, user_in: UserUpdateMe) -> User:
        # Implementar lógica de actualización del propio usuario
        pass

    async def delete_user(self, user_id: int) -> None:
        # Implementar lógica de eliminación de usuario
        pass

user_service = UserService()