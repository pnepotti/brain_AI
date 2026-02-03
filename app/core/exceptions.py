# app/core/exceptions.py
from fastapi import HTTPException, status


class AppException(Exception):
    """Clase base para excepciones de la aplicación."""
    
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserAlreadyExistsError(AppException):
    def __init__(self, message: str = "Usuario ya existe"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class UserNotFoundError(AppException):
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class InvalidCredentialsError(AppException):
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class InactiveUserError(AppException):
    def __init__(self, message: str = "Usuario inactivo"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Acceso prohibido"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)