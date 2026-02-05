"""
EJEMPLO DE USO DE get_current_user EN OTROS ENDPOINTS
Este archivo muestra cómo proteger endpoints requiriendo autenticación JWT.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

# Ejemplos de cómo usar get_current_user en diferentes endpoints:

# 1. ENDPOINT PROTEGIDO - Solo usuario autenticado
# @router.get("/me", response_model=UserResponse)
# async def get_current_user_info(current_user: User = Depends(get_current_user)):
#     """
#     Obtiene la información del usuario autenticado.
#     Requiere: Token JWT válido en header Authorization: Bearer <token>
#     """
#     return current_user


# 2. ENDPOINT CON ACCESO A BD Y USUARIO
# @router.patch("/me")
# async def update_current_user(
#     data: UserUpdateMe,
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Actualiza el perfil del usuario autenticado.
#     Requiere: Token JWT válido
#     """
#     current_user.full_name = data.full_name
#     db.add(current_user)
#     await db.commit()
#     await db.refresh(current_user)
#     return current_user


# 3. ENDPOINT CON VALIDACIÓN DE ROL (Admin only)
# @router.delete("/{user_id}")
# async def delete_user_admin_only(
#     user_id: int,
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Elimina un usuario (solo admin).
#     Requiere: Token JWT válido + rol ADMIN
#     """
#     if current_user.role != "admin":
#         raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar usuarios")
#     
#     # ... lógica de eliminación


# 4. CREAR DEPENDENCY PERSONALIZADA PARA ROL
# from typing import Callable
# from fastapi import HTTPException, status
# 
# def require_role(required_role: str) -> Callable:
#     """
#     Factory para crear dependency que requiere un rol específico.
#     Uso: Depends(require_role("admin"))
#     """
#     async def check_role(current_user: User = Depends(get_current_user)) -> User:
#         if current_user.role != required_role:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Se requiere rol {required_role}"
#             )
#         return current_user
#     return check_role
#
# @router.delete("/{user_id}")
# async def delete_user(user_id: int, current_user: User = Depends(require_role("admin"))):
#     """Elimina un usuario (solo admin)"""
#     pass


# 5. DEPENDENCY PARA VALIDAR MÚLTIPLES ROLES
# def require_any_role(allowed_roles: list[str]) -> Callable:
#     """Requiere que el usuario tenga uno de los roles especificados"""
#     async def check_roles(current_user: User = Depends(get_current_user)) -> User:
#         if current_user.role not in allowed_roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Se requiere uno de los roles: {', '.join(allowed_roles)}"
#             )
#         return current_user
#     return check_roles
#
# @router.post("/")
# async def create_resource(current_user: User = Depends(require_any_role(["admin", "doctor"]))):
#     """Crea un recurso (admin o doctor)"""
#     pass
