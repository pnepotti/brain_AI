from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.api import router as api_router
from app.core.exceptions import AppException, ErrorCode
from app.core.config import settings

from app.db.session import AsyncSessionLocal
from app.core.init_admin_user import init_admin_user

logger = logging.getLogger(__name__)


# CREACIÓN DE USUARIO ADMIN AL INICIAR (si no existe)



# LIFESPAN DEinit_user_admin.py LA APLICACIÓN

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    logger.info("🚀 Starting application initialization...")
    
    async with AsyncSessionLocal() as db:
        try:
            await init_admin_user(db)
        except Exception as e:
            logger.critical(f"❌ Critical error during startup: {e}")
            raise e
    
    yield 

    # --- SHUTDOWN ---
    logger.info("🛑 Application shutdown.")


# CONFIGURACIÓN DE APLICACIÓN

app = FastAPI(
    title="Brain MRI Service",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)


# EXCEPTION HANDLERS - CENTRALIZADOS

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handler para todas las excepciones de negocio."""
    logger.warning(
        f"AppException | Code: {exc.error_code} | Status: {exc.status_code} | "
        f"Path: {request.url.path} | Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code.value,
            "detail": exc.message
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler global para excepciones no controladas."""
    logger.error(
        f"Unhandled exception: {type(exc).__name__} | "
        f"Path: {request.url.path} | Method: {request.method}",
        exc_info=exc
    )
    
    detail = "Error interno del servidor" if not settings.DEBUG else str(exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": ErrorCode.INTERNAL_SERVER_ERROR.value,
            "detail": detail
        }
    )


# ROUTERS

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raíz para verificar que la API está en funcionamiento.
    """
    return {"message": "Welcome to Brain MRI Service API"}