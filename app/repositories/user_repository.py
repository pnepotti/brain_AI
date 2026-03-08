from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from typing import Optional


class UserRepository:
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def update_by_id(
        self, 
        db: AsyncSession, 
        user_id: int, 
        **kwargs
    ) -> Optional[User]:
        """Actualiza campos específicos."""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def delete_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Elimina y retorna el usuario eliminado."""
        user = await self.get_by_id(db, user_id)
        if not user:
            return None
        
        await db.delete(user)
        await db.commit()
        return user
    
    
user_repository = UserRepository()
    