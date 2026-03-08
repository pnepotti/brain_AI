from app.core.config import settings
from app.db.session import AsyncSession
from app.models.user import User, UserRole
from app.core.security_utils import get_password_hash
import logging
from app.repositories.user_repository import user_repository


logger = logging.getLogger(__name__)

async def init_admin_user(db: AsyncSession):
    """
    Verifica si el admin existe al iniciar. 
    Usa las variables de entorno cargadas en settings.
    """
    admin_email = settings.ADMIN_EMAIL

    user = await user_repository.get_by_email(db, admin_email)
    if not user:
        logger.info(f"Admin user not found. Creating default admin: {admin_email}")
        try:
            hashed_password = get_password_hash(settings.ADMIN_PASSWORD.get_secret_value())
            user = User(
                email=admin_email,
                password_hash=hashed_password,
                role=UserRole.ADMIN.value,
                full_name="Admin User", 
                is_active=True
            )
            await user_repository.create(db, user)  
            logger.info("✅ Admin user created successfully.")
        except Exception as e:
            logger.error(f"Failed to create admin user: {e}")
            await db.rollback()
    else:
        logger.info(f"ℹ️ Admin user {admin_email} already exists.")
