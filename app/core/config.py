from pydantic_settings import BaseSettings
from pydantic import EmailStr, SecretStr

class Settings(BaseSettings):
    # Ambiente
    DEBUG: bool = False
    
    # Base de Datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_SERVER: str
    POSTGRES_DB: str

    # Seguridad
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Administrador
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: SecretStr

    # Rutas de archivos
    UPLOADS_DIR: str = "uploads"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        # .get_secret_value() es necesario para acceder al valor de SecretStr
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = False 

settings = Settings()