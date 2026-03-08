# 📋 Guía de Manejo de Excepciones - FastAPI Clean Architecture

## Resumen de Mejores Prácticas Implementadas

### 1. ✅ Excepciones Centralizadas (`app/core/exceptions.py`)

**Ventajas:**
- Todos los códigos de error en un solo lugar
- Mensajes estandarizados reutilizables
- Cambios en mensajes no afectan múltiples archivos

**Estructura:**
```python
class ErrorCode(str, Enum):
    """Códigos de error únicos"""
    USER_NOT_FOUND = "USER_NOT_FOUND"

class ErrorMessages:
    """Mensajes por defecto"""
    USER_NOT_FOUND = "Usuario no encontrado"

class ParticularError(AppException):
    def __init__(self, message: str = ErrorMessages.USER_NOT_FOUND):
        super().__init__(message, status.HTTP_404_NOT_FOUND, ErrorCode.USER_NOT_FOUND)
```

---

### 2. ✅ Exception Handlers Globales (`app/main.py`)

**Patrón:**
```python
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    # Aquí se capturan TODAS las excepciones de negocio
    logger.warning(f"AppException | Code: {exc.error_code}...")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code.value, "detail": exc.message}
    )
```

**Beneficios:**
- No necesitas try-catch en cada endpoint
- Consistencia en respuestas
- Logging centralizado

---

### 3. ✅ Servicios - Lanzar Excepciones

**Patrón CORRECTO** (ahora implementado):
```python
#❌ MAL - No hagas esto
@router.post("/")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await user_service.create_user(db, data)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

# ✅ BIEN - Así se hace
@router.post("/")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, data)  # Deja que FastAPI maneje
```

**En el servicio:**
```python
class UserService:
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        if user_exists:
            raise UserAlreadyExistsError(f"Email {email} ya registrado")
        # ... resto del código
```

---

### 4. ✅ Respuesta JSON Consistente

**Respuesta de éxito:**
```json
{
    "access_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 1800
}
```

**Respuesta de error:**
```json
{
    "error": "USER_NOT_FOUND",
    "detail": "Usuario no encontrado"
}
```

**Ventaja:** El cliente siempre sabe qué esperar

---

### 5. 📊 Flujo de Excepciones en FastAPI

```
USER REQUEST
    ↓
    ├─ Endpoint (sin try-catch)
    │   ↓
    │   └─ Servicio lanza AppException
    │       ↓
    │       ❌ Excepción NO se captura en endpoint
    │
    ├─ FastAPI detecta AppException
    │   ↓
    │   └─ Exception Handler Global (@app.exception_handler)
    │       ↓
    │       └─ JSONResponse consistente
    │
    └─ Response JSON al cliente
```

---

### 6. 📝 Checklist para Nuevas Excepciones

Cuando agregues una nueva excepción:

- [ ] Añadir `ErrorCode` en [exceptions.py](app/core/exceptions.py#L7)
- [ ] Añadir mensaje en `ErrorMessages` en [exceptions.py](app/core/exceptions.py#L17)
- [ ] Crear clase de excepción en [exceptions.py](app/core/exceptions.py#L28)
- [ ] **NO** añadir try-catch en endpoints
- [ ] **SÍ** lanzar la excepción en servicios

**Ejemplo:**
```python
# En exceptions.py
class ErrorCode(str, Enum):
    INVALID_FILE = "INVALID_FILE"

class ErrorMessages:
    INVALID_FILE = "El archivo debe ser .pdf"

class InvalidFileError(AppException):
    def __init__(self, msg: str = ErrorMessages.INVALID_FILE):
        super().__init__(msg, status.HTTP_400_BAD_REQUEST, ErrorCode.INVALID_FILE)

# En servicio
if not is_valid_file(file):
    raise InvalidFileError()  # Se captura automáticamente

# En endpoint - ¡SIN try-catch!
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    return await service.process_file(file)
```

---

### 7. 🚀 Ventajas de Esta Arquitectura

| Aspecto | Antes | Ahora |
|--------|--------|-------|
| **Duplicación** | ❌ Código en múltiples lugares | ✅ Centralizado |
| **Consistencia** | ❌ Respuestas inconsistentes | ✅ Formato único |
| **Mantenimiento** | ❌ Cambiar mensaje = editar N archivos | ✅ Un archivo |
| **Legibilidad** | ❌ try-catch en cada endpoint | ✅ Código limpio |
| **Testing** | ❌ Difícil testear handlers | ✅ Fácil mockear |
| **Logging** | ❌ Disperso | ✅ Centralizado |

---

### 8. 📚 Referencias FastAPI

- [Exception Handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#add-custom-exception-handlers)
- [HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body)
- [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)

---

## Archivos Modificados

1. **[app/core/exceptions.py](app/core/exceptions.py)** - Añadido `ErrorMessages` para centralizar mensajes
2. **[app/main.py](app/main.py)** - Limpieza y comentarios
3. **[app/api/v1/endpoints/auth.py](app/api/v1/endpoints/auth.py)** - Eliminados try-catch innecesarios
4. **[app/api/v1/endpoints/user.py](app/api/v1/endpoints/user.py)** - Eliminados try-catch innecesarios
5. **[app/services/user_service.py](app/services/user_service.py)** - Usa excepciones centralizadas

---

## Siguiente Paso

Para endpoints futuros, recuerda:

```python
# ✅ PATRÓN CORRECTO
@router.post("/endpoint")
async def my_endpoint(db: AsyncSession = Depends(get_db)):
    """Sin try-catch - FastAPI maneja las excepciones automáticamente"""
    result = await my_service.do_something(db)
    return result
```

