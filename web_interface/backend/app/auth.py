"""
🔐 SISTEMA DE AUTENTICACIÓN - Adventure Game Web Interface
JWT Authentication and authorization system
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets
import logging

logger = logging.getLogger(__name__)

# Configuración de JWT
SECRET_KEY = secrets.token_urlsafe(32)  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Configuración de encriptación de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de seguridad
security = HTTPBearer()

# Base de datos de usuarios (en producción, usar BD real)
USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),  # Password: admin123
        "role": "admin",
        "permissions": ["read", "write", "backup", "config", "system"],
        "created_at": datetime.now(),
        "last_login": None,
        "active": True
    },
    "operator": {
        "username": "operator", 
        "hashed_password": pwd_context.hash("operator123"),  # Password: operator123
        "role": "operator",
        "permissions": ["read", "backup"],
        "created_at": datetime.now(),
        "last_login": None,
        "active": True
    },
    "viewer": {
        "username": "viewer",
        "hashed_password": pwd_context.hash("viewer123"),  # Password: viewer123
        "role": "viewer",
        "permissions": ["read"],
        "created_at": datetime.now(),
        "last_login": None,
        "active": True
    }
}

class AuthManager:
    """Gestor de autenticación y autorización"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hashea una contraseña"""
        return pwd_context.hash(password)
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica un usuario"""
        user = USERS_DB.get(username)
        if not user:
            return None
        if not user["active"]:
            return None
        if not AuthManager.verify_password(password, user["hashed_password"]):
            return None
        
        # Actualizar último login
        user["last_login"] = datetime.now()
        
        return user
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Crea un token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verifica un token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            
            # Verificar que el usuario existe y está activo
            user = USERS_DB.get(username)
            if not user or not user["active"]:
                return None
                
            return {
                "username": username,
                "role": user["role"],
                "permissions": user["permissions"],
                "exp": payload.get("exp")
            }
        except JWTError:
            return None
    
    @staticmethod
    def check_permission(user: Dict[str, Any], required_permission: str) -> bool:
        """Verifica si un usuario tiene un permiso específico"""
        if not user:
            return False
        return required_permission in user.get("permissions", [])
    
    @staticmethod
    def create_user(username: str, password: str, role: str, permissions: list) -> bool:
        """Crea un nuevo usuario"""
        if username in USERS_DB:
            return False
        
        USERS_DB[username] = {
            "username": username,
            "hashed_password": AuthManager.get_password_hash(password),
            "role": role,
            "permissions": permissions,
            "created_at": datetime.now(),
            "last_login": None,
            "active": True
        }
        return True
    
    @staticmethod
    def update_user_password(username: str, new_password: str) -> bool:
        """Actualiza la contraseña de un usuario"""
        if username not in USERS_DB:
            return False
        
        USERS_DB[username]["hashed_password"] = AuthManager.get_password_hash(new_password)
        return True
    
    @staticmethod
    def deactivate_user(username: str) -> bool:
        """Desactiva un usuario"""
        if username not in USERS_DB:
            return False
        
        USERS_DB[username]["active"] = False
        return True
    
    @staticmethod
    def get_user_info(username: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un usuario"""
        user = USERS_DB.get(username)
        if not user:
            return None
        
        # Retornar información sin la contraseña hasheada
        return {
            "username": user["username"],
            "role": user["role"],
            "permissions": user["permissions"],
            "created_at": user["created_at"],
            "last_login": user["last_login"],
            "active": user["active"]
        }
    
    @staticmethod
    def list_users() -> list:
        """Lista todos los usuarios"""
        return [
            AuthManager.get_user_info(username) 
            for username in USERS_DB.keys()
        ]

class PermissionChecker:
    """Decoradores y funciones para verificar permisos"""
    
    @staticmethod
    def require_permission(permission: str):
        """Decorador para requerir un permiso específico"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Obtener usuario del contexto
                current_user = kwargs.get("current_user")
                if not current_user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Usuario no autenticado"
                    )
                
                if not AuthManager.check_permission(current_user, permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permiso requerido: {permission}"
                    )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def require_role(role: str):
        """Decorador para requerir un rol específico"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                current_user = kwargs.get("current_user")
                if not current_user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Usuario no autenticado"
                    )
                
                if current_user.get("role") != role:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Rol requerido: {role}"
                    )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Dependencias para FastAPI
async def get_current_user(credentials: HTTPAuthorizationCredentials = security) -> Dict[str, Any]:
    """Dependencia para obtener el usuario actual"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        user = AuthManager.verify_token(token)
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception

async def get_current_active_user(current_user: Dict[str, Any] = get_current_user) -> Dict[str, Any]:
    """Dependencia para obtener usuario activo"""
    user_info = AuthManager.get_user_info(current_user["username"])
    if not user_info or not user_info["active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    return current_user

# Dependencias de permisos específicos
async def require_read_permission(current_user: Dict[str, Any] = get_current_active_user) -> Dict[str, Any]:
    """Requiere permiso de lectura"""
    if not AuthManager.check_permission(current_user, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso de lectura requerido"
        )
    return current_user

async def require_write_permission(current_user: Dict[str, Any] = get_current_active_user) -> Dict[str, Any]:
    """Requiere permiso de escritura"""
    if not AuthManager.check_permission(current_user, "write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso de escritura requerido"
        )
    return current_user

async def require_backup_permission(current_user: Dict[str, Any] = get_current_active_user) -> Dict[str, Any]:
    """Requiere permiso de backup"""
    if not AuthManager.check_permission(current_user, "backup"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso de backup requerido"
        )
    return current_user

async def require_config_permission(current_user: Dict[str, Any] = get_current_active_user) -> Dict[str, Any]:
    """Requiere permiso de configuración"""
    if not AuthManager.check_permission(current_user, "config"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso de configuración requerido"
        )
    return current_user

async def require_system_permission(current_user: Dict[str, Any] = get_current_active_user) -> Dict[str, Any]:
    """Requiere permiso de sistema"""
    if not AuthManager.check_permission(current_user, "system"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permiso de sistema requerido"
        )
    return current_user

async def require_admin_role(current_user: Dict[str, Any] = get_current_active_user) -> Dict[str, Any]:
    """Requiere rol de administrador"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol de administrador requerido"
        )
    return current_user

# Función para inicializar usuarios por defecto
def initialize_default_users():
    """Inicializa usuarios por defecto"""
    logger.info("🔐 Inicializando sistema de autenticación...")
    logger.info("👥 Usuarios disponibles:")
    for username, user in USERS_DB.items():
        logger.info(f"   • {username} ({user['role']}) - Permisos: {user['permissions']}")
    
    logger.info("🔑 Credenciales por defecto:")
    logger.info("   • admin:admin123 (admin completo)")
    logger.info("   • operator:operator123 (lectura + backup)")
    logger.info("   • viewer:viewer123 (solo lectura)")

if __name__ == "__main__":
    # Test del sistema de autenticación
    initialize_default_users()
    
    # Probar autenticación
    print("\n🧪 Probando autenticación...")
    
    # Test login válido
    user = AuthManager.authenticate_user("admin", "admin123")
    if user:
        print("✅ Login admin exitoso")
        
        # Crear token
        token = AuthManager.create_access_token({"sub": user["username"]})
        print(f"🔑 Token generado: {token[:20]}...")
        
        # Verificar token
        verified_user = AuthManager.verify_token(token)
        if verified_user:
            print("✅ Token verificado exitosamente")
            print(f"   Usuario: {verified_user['username']}")
            print(f"   Rol: {verified_user['role']}")
            print(f"   Permisos: {verified_user['permissions']}")
        else:
            print("❌ Error verificando token")
    else:
        print("❌ Error en login admin")
    
    # Test login inválido
    user = AuthManager.authenticate_user("admin", "wrongpassword")
    if not user:
        print("✅ Login inválido correctamente rechazado")
    else:
        print("❌ Login inválido aceptado (ERROR)")
    
    print("\n🏆 Sistema de autenticación listo!")
