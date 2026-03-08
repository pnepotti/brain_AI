# app/core/exceptions.py
from fastapi import status
from enum import Enum


# ============================================
# CÓDIGOS DE ERROR CENTRALIZADOS
# ============================================
class ErrorCode(str, Enum):
    """Códigos de error estandarizados para la API."""
    # Usuarios
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INACTIVE_USER = "INACTIVE_USER"
    # Análisis
    INVALID_IMAGE = "INVALID_IMAGE"
    MISSING_PATIENT = "MISSING_PATIENT"
    ANALYSIS_NOT_FOUND = "ANALYSIS_NOT_FOUND"
    # Pacientes
    PATIENT_NOT_FOUND = "PATIENT_NOT_FOUND"
    # General
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


# ============================================
# MENSAJES DE ERROR CENTRALIZADOS
# ============================================
class ErrorMessages:
    """Mensajes de error estandarizados."""
    # Usuarios
    USER_ALREADY_EXISTS = "Usuario ya existe"
    USER_NOT_FOUND = "Usuario no encontrado"
    INVALID_CREDENTIALS = "Credenciales inválidas"
    INACTIVE_USER = "Usuario inactivo"
    # Análisis
    INVALID_IMAGE = "Formato de imagen inválido"
    MISSING_PATIENT = "ID de paciente es requerido"
    ANALYSIS_NOT_FOUND = "Análisis no encontrado"
    # Pacientes
    PATIENT_NOT_FOUND = "Paciente no encontrado"
    
    # General
    UNAUTHORIZED = "No autorizado"
    FORBIDDEN = "Acceso prohibido"
    INTERNAL_SERVER_ERROR = "Error interno del servidor"


# ============================================
# EXCEPCIONES PERSONALIZADAS
# ============================================
class AppException(Exception):
    """Clase base para excepciones de la aplicación."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: ErrorCode = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or ErrorCode.INTERNAL_SERVER_ERROR
        super().__init__(self.message)

# ============================================
# EXCEPCIONES DE USUARIOS
# ============================================

class UserAlreadyExistsError(AppException):
    def __init__(self, message: str = ErrorMessages.USER_ALREADY_EXISTS):
        super().__init__(message, status.HTTP_409_CONFLICT, ErrorCode.USER_ALREADY_EXISTS)


class UserNotFoundError(AppException):
    def __init__(self, message: str = ErrorMessages.USER_NOT_FOUND):
        super().__init__(message, status.HTTP_404_NOT_FOUND, ErrorCode.USER_NOT_FOUND)


class InvalidCredentialsError(AppException):
    def __init__(self, message: str = ErrorMessages.INVALID_CREDENTIALS):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, ErrorCode.INVALID_CREDENTIALS)


class InactiveUserError(AppException):
    def __init__(self, message: str = ErrorMessages.INACTIVE_USER):
        super().__init__(message, status.HTTP_403_FORBIDDEN, ErrorCode.INACTIVE_USER)


class UnauthorizedError(AppException):
    def __init__(self, message: str = ErrorMessages.UNAUTHORIZED):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, ErrorCode.UNAUTHORIZED)


class ForbiddenError(AppException):
    def __init__(self, message: str = ErrorMessages.FORBIDDEN):
        super().__init__(message, status.HTTP_403_FORBIDDEN, ErrorCode.FORBIDDEN)


# ============================================
# EXCEPCIONES DE ANÁLISIS
# ============================================
class InvalidImageError(AppException):
    def __init__(self, message: str = ErrorMessages.INVALID_IMAGE):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, ErrorCode.INVALID_IMAGE)


class MissingPatientError(AppException):
    def __init__(self, message: str = ErrorMessages.MISSING_PATIENT):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, ErrorCode.MISSING_PATIENT)


class AnalysisNotFoundError(AppException):
    def __init__(self, message: str = ErrorMessages.ANALYSIS_NOT_FOUND):
        super().__init__(message, status.HTTP_404_NOT_FOUND, ErrorCode.ANALYSIS_NOT_FOUND)

# ============================================
# EXCEPCIONES DE PACIENTES
# ============================================
class PatientNotFoundError(AppException):
    def __init__(self, message: str = ErrorMessages.PATIENT_NOT_FOUND):
        super().__init__(message, status.HTTP_404_NOT_FOUND, ErrorCode.PATIENT_NOT_FOUND)