from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    """Esquema para login request."""
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class TokenResponse(BaseModel):
    """Esquema para respuesta de token."""
    access_token: str
    token_type: str  # siempre "bearer"
    expires_in: int  # segundos hasta expiración
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class RefreshTokenRequest(BaseModel):
    """Esquema para refresh token request."""
    refresh_token: Optional[str] = None
    # En mi caso, el refresh_token viene del JWT (via get_current_user)