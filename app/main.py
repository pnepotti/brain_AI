from fastapi import FastAPI
from app.api.v1.api import router as api_router
import logging
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(title="Brain MRI Service", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")