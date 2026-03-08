#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos iniciales (seeds).
Se ejecuta después de las migraciones.
"""
import asyncio
import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar modelos y servicios
from app.models.user import User, UserRole
from app.core.security_utils import get_password_hash


async def init_admin_user():
    """Crear usuario admin si no existe."""
    
    # Configurar conexión a BD
    database_url = (
        f"postgresql+asyncpg://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_SERVER')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )
    
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            query = select(User).where(User.email == os.getenv("ADMIN_EMAIL"))
            result = await session.execute(query)
            existing_admin = result.scalars().first()
            
            if existing_admin:
                logger.info(f"✓ Usuario admin ya existe: {os.getenv('ADMIN_EMAIL')}")
                return
            
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")
            
            if not admin_email or not admin_password:
                logger.error("❌ Variable ADMIN_EMAIL o ADMIN_PASSWORD no configuradas")
                raise ValueError("Credenciales de admin no configuradas en .env")
            
            hashed_password = get_password_hash(admin_password)
            
            admin_user = User(
                email=admin_email,
                password_hash=hashed_password,
                full_name="Administrator",
                is_active=True,
                role=UserRole.ADMIN.value
            )
            
            session.add(admin_user)
            await session.commit()
            
            logger.info(f"✓ Usuario admin creado exitosamente: {admin_email}")
            
        except Exception as e:
            logger.error(f"❌ Error creando usuario admin: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


async def main():
    """Ejecutar inicialización."""
    try:
        await init_admin_user()
        logger.info("✓ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error durante la inicialización: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
