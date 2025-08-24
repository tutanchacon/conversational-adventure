"""
🌐 ADVENTURE GAME WEB INTERFACE - Backend API (Versión de Desarrollo)
Versión simplificada para desarrollo y testing
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    """Gestor de conexiones WebSocket para tiempo real"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Cliente WebSocket conectado. Total: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Cliente WebSocket desconectado. Total: {len(self.active_connections)}")
        
    async def broadcast(self, message: dict):
        """Envía mensaje a todos los clientes conectados"""
        if self.active_connections:
            message_str = json.dumps(message, default=str)
            disconnected = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_str)
                except:
                    disconnected.append(connection)
            
            # Limpiar conexiones muertas
            for connection in disconnected:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

class SystemManager:
    """Gestor del sistema Adventure Game (versión desarrollo)"""
    
    def __init__(self):
        self.websocket_manager = WebSocketManager()
        self.system_stats = {
            "uptime": datetime.now(),
            "requests_count": 0,
            "active_sessions": 0,
            "last_backup": None,
            "system_health": "healthy"
        }
        self.mock_backups = [
            {
                "backup_id": "backup_20250823_120000",
                "timestamp": datetime.now() - timedelta(hours=2),
                "size_bytes": 108311,
                "files_count": 37,
                "backup_type": "auto",
                "integrity_hash": "a1b2c3d4e5f6...",
                "game_state_summary": "Events: 1205, Last: 2025-08-23 12:00:00"
            },
            {
                "backup_id": "backup_20250823_060000", 
                "timestamp": datetime.now() - timedelta(hours=8),
                "size_bytes": 105467,
                "files_count": 35,
                "backup_type": "auto",
                "integrity_hash": "f6e5d4c3b2a1...",
                "game_state_summary": "Events: 1180, Last: 2025-08-23 06:00:00"
            }
        ]
        
    async def initialize(self):
        """Inicializa todos los componentes del sistema"""
        try:
            logger.info("🚀 Inicializando sistema Adventure Game (modo desarrollo)...")
            
            # Simular inicialización
            await asyncio.sleep(0.5)
            
            logger.info("✅ Sistema inicializado correctamente")
            
            # Enviar notificación por WebSocket
            await self.websocket_manager.broadcast({
                "type": "system_status",
                "status": "initialized",
                "timestamp": datetime.now().isoformat(),
                "message": "Sistema Adventure Game inicializado (modo desarrollo)"
            })
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            self.system_stats["system_health"] = "error"
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas del sistema en tiempo real"""
        try:
            uptime = datetime.now() - self.system_stats["uptime"]
            
            # Métricas simuladas para desarrollo
            metrics = {
                "uptime_seconds": int(uptime.total_seconds()),
                "uptime_formatted": str(uptime).split('.')[0],
                "requests_count": self.system_stats["requests_count"],
                "active_websockets": len(self.websocket_manager.active_connections),
                "system_health": self.system_stats["system_health"],
                "timestamp": datetime.now().isoformat(),
                "events_count": 1234,
                "total_backups": len(self.mock_backups),
                "last_backup": self.mock_backups[0]["timestamp"] if self.mock_backups else None
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def increment_requests(self):
        """Incrementa contador de requests"""
        self.system_stats["requests_count"] += 1

# Instancia global del gestor
system_manager = SystemManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    await system_manager.initialize()
    
    # Iniciar tarea de métricas en tiempo real
    metrics_task = asyncio.create_task(metrics_broadcaster())
    
    yield
    
    # Shutdown
    metrics_task.cancel()
    logger.info("🛑 Sistema Adventure Game detenido")

async def metrics_broadcaster():
    """Envía métricas del sistema cada 5 segundos"""
    while True:
        try:
            await asyncio.sleep(5)
            metrics = await system_manager.get_system_metrics()
            await system_manager.websocket_manager.broadcast({
                "type": "metrics_update",
                "data": metrics
            })
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error en broadcaster de métricas: {e}")

# Crear aplicación FastAPI
app = FastAPI(
    title="Adventure Game Web Interface",
    description="Professional web administration for Adventure Game v1.1.0",
    version="2.0.0-dev",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para tracking de requests
@app.middleware("http")
async def track_requests(request, call_next):
    system_manager.increment_requests()
    response = await call_next(request)
    return response

# Security simplificado para desarrollo
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificación de autenticación simplificada para desarrollo"""
    if credentials.credentials in ["admin-token", "dev-token"]:
        return {"username": "admin", "role": "admin", "permissions": ["read", "write", "backup", "config", "system"]}
    raise HTTPException(status_code=401, detail="Token inválido")

# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Adventure Game Web Interface API",
        "version": "2.0.0-dev",
        "status": "running",
        "mode": "development",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": str(datetime.now() - system_manager.system_stats["uptime"]).split('.')[0],
        "mode": "development"
    }

@app.get("/api/metrics")
async def get_metrics():
    """Obtiene métricas del sistema (sin autenticación para desarrollo)"""
    return await system_manager.get_system_metrics()

@app.get("/api/system/status")
async def get_system_status():
    """Estado detallado del sistema (sin autenticación para desarrollo)"""
    return {
        "adventure_game": {
            "status": "running",
            "memory_system": True,
            "mcp_provider": True,
            "mode": "development"
        },
        "backup_system": {
            "status": "running",
            "manager": True,
            "restore": True
        },
        "websockets": {
            "active_connections": len(system_manager.websocket_manager.active_connections)
        }
    }

@app.get("/api/backups")
async def list_backups():
    """Lista todos los backups disponibles (mock data)"""
    return [
        {
            **backup,
            "timestamp": backup["timestamp"].isoformat(),
            "integrity_hash": backup["integrity_hash"][:16] + "..."
        }
        for backup in system_manager.mock_backups
    ]

@app.post("/api/backups/create")
async def create_backup(backup_type: str = "manual"):
    """Crea un nuevo backup (simulado)"""
    new_backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Simular creación de backup
    await asyncio.sleep(1)
    
    # Agregar a la lista mock
    new_backup = {
        "backup_id": new_backup_id,
        "timestamp": datetime.now(),
        "size_bytes": 109500,
        "files_count": 38,
        "backup_type": backup_type,
        "integrity_hash": "new123backup456...",
        "game_state_summary": f"Events: 1250, Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }
    system_manager.mock_backups.insert(0, new_backup)
    
    # Notificar por WebSocket
    await system_manager.websocket_manager.broadcast({
        "type": "backup_created",
        "backup_id": new_backup_id,
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True, "backup_id": new_backup_id}

@app.get("/api/events")
async def get_events(limit: int = 100, offset: int = 0):
    """Obtiene eventos del sistema de memoria (mock data)"""
    mock_events = [
        {
            "event_id": f"event_{i}",
            "timestamp": datetime.now() - timedelta(minutes=i*5),
            "event_type": "game_action",
            "data": {"action": f"action_{i}", "value": i * 10},
            "user_id": "user_1" if i % 2 == 0 else "user_2"
        }
        for i in range(min(limit, 50))
    ]
    
    return {
        "events": [
            {
                **event,
                "timestamp": event["timestamp"].isoformat()
            }
            for event in mock_events[offset:offset+limit]
        ],
        "limit": limit,
        "offset": offset,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/auth/login")
async def login(credentials: dict):
    """Login endpoint (simplificado para desarrollo)"""
    username = credentials.get("username")
    password = credentials.get("password")
    
    # Credenciales de desarrollo
    if username == "admin" and password == "admin123":
        return {
            "success": True,
            "token": "admin-token",
            "user_info": {
                "username": "admin",
                "role": "admin",
                "permissions": ["read", "write", "backup", "config", "system"]
            },
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
    elif username == "dev" and password == "dev123":
        return {
            "success": True,
            "token": "dev-token", 
            "user_info": {
                "username": "dev",
                "role": "developer",
                "permissions": ["read", "write", "backup"]
            },
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para comunicación en tiempo real"""
    await system_manager.websocket_manager.connect(websocket)
    try:
        # Enviar estado inicial
        initial_data = {
            "type": "connection_established",
            "timestamp": datetime.now().isoformat(),
            "metrics": await system_manager.get_system_metrics()
        }
        await websocket.send_text(json.dumps(initial_data, default=str))
        
        # Mantener conexión viva
        while True:
            try:
                # Recibir mensajes del cliente (ping/pong)
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }))
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error en WebSocket: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        system_manager.websocket_manager.disconnect(websocket)

if __name__ == "__main__":
    print("🌐 ADVENTURE GAME WEB INTERFACE v2.0.0-dev")
    print("=" * 60)
    print("🚀 Iniciando servidor backend de desarrollo...")
    print("📊 Dashboard: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("🔑 Credenciales: admin:admin123 o dev:dev123")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
