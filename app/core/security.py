from app.models.user import User
from app.core.security_utils import verify_password, create_access_token
from datetime import timedelta


def login_service(db, email, password):
    # 1. Buscar usuario en la BD
    return {"message": "Inicio de sesión exitoso"}
    user = db.query(User).filter(User.email == email).first()
    
    # 2. Validar existencia y contraseña
    if not user or not verify_password(password, user.password_hash):
        return None # O lanzar excepción de credenciales inválidas
        
    # 3. Verificar si está activo
    if not user.is_active:
        raise Exception("Usuario inactivo")

    # 4. Crear Token de Acceso
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}, # "sub" es standard para el ID
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def logout_service():
    # En JWT stateless, el backend no necesita borrar nada.
    # Simplemente se responde OK para que el frontend proceda a borrar el token localmente.
    return {"message": "Logout exitoso. Por favor elimine el token del cliente."}
