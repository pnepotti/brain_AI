from sqlalchemy.future import select
from app.models.user import User
from .security_utils import verify_password, create_access_token
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

async def login_service(db: AsyncSession, email: str, password: str):
    # 1. Search user by email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    # 2. Verify password
    if not user or not verify_password(password, user.password_hash):
        return None 
        
    # 3. Check if user is active
    if not user.is_active:
        raise Exception("Usuario inactivo")

    # 4. Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def logout_service():
    # En JWT stateless, el backend no necesita borrar nada.
    # Simplemente se responde OK para que el frontend proceda a borrar el token localmente.
    return {"message": "Logout exitoso. Por favor elimine el token del cliente."}
