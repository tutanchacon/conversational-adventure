"""
🌐 ADVENTURE GAME WEB INTERFACE - Backend API
FastAPI application for professional web administration

Features:
🔐 JWT Authentication
📊 Real-time metrics
💾 Backup management  
🎮 Game control
📝 Logs and debugging
⚙️ Configuration management
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar nuestros módulos
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

try:
    from backup_system import BackupManager, RestoreManager, BackupConfig
    BACKUP_AVAILABLE = True
except ImportError:
    BACKUP_AVAILABLE = False
    BackupManager = RestoreManager = BackupConfig = None

try:
    from memory_system import PerfectMemorySystem
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    PerfectMemorySystem = None

try:
    from enhanced_mcp import EnhancedMCPProvider
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    EnhancedMCPProvider = None

try:
    from multiplayer.websocket_handler import websocket_manager, websocket_endpoint
    from multiplayer.multiplayer_game import get_multiplayer_game
    MULTIPLAYER_AVAILABLE = True
except ImportError:
    MULTIPLAYER_AVAILABLE = False
    websocket_manager = websocket_endpoint = get_multiplayer_game = None

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración global
FRONTEND_BUILD_DIR = Path(__file__).parent.parent / "frontend" / "build"

class WebSocketManager:
    """Gestor de conexiones WebSocket para tiempo real"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Cliente WebSocket conectado. Total: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Cliente WebSocket desconectado. Total: {len(self.active_connections)}")
        
    async def broadcast(self, message: dict):
        """Envía mensaje a todos los clientes conectados"""
        if self.active_connections:
            message_str = json.dumps(message)
            disconnected = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(message_str)
                except:
                    disconnected.append(connection)
            
            # Limpiar conexiones muertas
            for connection in disconnected:
                self.active_connections.remove(connection)

class SystemManager:
    """Gestor del sistema Adventure Game"""
    
    def __init__(self):
        self.backup_manager = None
        self.restore_manager = None
        self.memory_system = None
        self.mcp_provider = None
        self.websocket_manager = WebSocketManager()
        self.system_stats = {
            "uptime": datetime.now(),
            "requests_count": 0,
            "active_sessions": 0,
            "last_backup": None,
            "system_health": "healthy"
        }
        
    async def initialize(self):
        """Inicializa todos los componentes del sistema"""
        try:
            logger.info("🚀 Inicializando sistema Adventure Game...")
            
            # Inicializar sistema de backup si está disponible
            if BACKUP_AVAILABLE:
                backup_config = BackupConfig()
                self.backup_manager = BackupManager(backup_config)
                self.restore_manager = RestoreManager(self.backup_manager)
                logger.info("✅ Sistema de backup inicializado")
            else:
                logger.warning("⚠️ Sistema de backup no disponible")
            
            # Inicializar sistema de memoria si está disponible
            if MEMORY_AVAILABLE:
                self.memory_system = PerfectMemorySystem()
                # El PerfectMemorySystem se inicializa automáticamente en __init__
                logger.info("✅ Sistema de memoria inicializado")
            else:
                logger.warning("⚠️ Sistema de memoria no disponible")
            
            # Inicializar MCP Provider si está disponible
            if MCP_AVAILABLE and self.memory_system:
                self.mcp_provider = EnhancedMCPProvider(self.memory_system)
                logger.info("✅ MCP Provider inicializado")
            else:
                logger.warning("⚠️ MCP Provider no disponible")
            
            # Inicializar sistema multi-jugador si está disponible
            if MULTIPLAYER_AVAILABLE and self.memory_system:
                try:
                    multiplayer_game = get_multiplayer_game()
                    await multiplayer_game.initialize_world()
                    logger.info("✅ Sistema multi-jugador inicializado")
                except Exception as e:
                    logger.warning(f"⚠️ Error inicializando multi-jugador: {e}")
                    logger.warning("⚠️ Continuando sin sistema multi-jugador")
            else:
                logger.warning("⚠️ Sistema multi-jugador no disponible")
            
            logger.info("✅ Sistema inicializado correctamente")
            
            # Enviar notificación por WebSocket
            await self.websocket_manager.broadcast({
                "type": "system_status",
                "status": "initialized",
                "timestamp": datetime.now().isoformat(),
                "message": "Sistema Adventure Game inicializado"
            })
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            self.system_stats["system_health"] = "error"
            # No re-lanzar la excepción para que el servidor pueda seguir funcionando
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas del sistema en tiempo real"""
        try:
            uptime = datetime.now() - self.system_stats["uptime"]
            
            # Métricas básicas
            metrics = {
                "uptime_seconds": int(uptime.total_seconds()),
                "uptime_formatted": str(uptime).split('.')[0],
                "requests_count": self.system_stats["requests_count"],
                "active_websockets": len(self.websocket_manager.active_connections),
                "system_health": self.system_stats["system_health"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Métricas de memoria si está disponible
            if self.memory_system:
                try:
                    # Contar eventos directamente de la base de datos
                    cursor = self.memory_system.db_connection.execute("SELECT COUNT(*) FROM game_events")
                    events_count = cursor.fetchone()[0]
                    metrics["events_count"] = events_count
                except:
                    metrics["events_count"] = 0
            
            # Métricas de backup si está disponible
            if self.backup_manager:
                try:
                    backups = self.backup_manager.list_backups()
                    metrics["total_backups"] = len(backups)
                    metrics["last_backup"] = backups[0].timestamp.isoformat() if backups else None
                except:
                    metrics["total_backups"] = 0
                    metrics["last_backup"] = None
            
            # Métricas multi-jugador si está disponible
            if MULTIPLAYER_AVAILABLE and websocket_manager:
                try:
                    multiplayer_stats = websocket_manager.get_connection_stats()
                    metrics["multiplayer"] = multiplayer_stats
                except:
                    metrics["multiplayer"] = {"error": "No disponible"}
            
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
    version="2.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
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

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificación de autenticación (simplificada para demo)"""
    # En producción, verificar JWT token aquí
    if credentials.credentials == "admin-token":
        return {"username": "admin", "role": "admin"}
    raise HTTPException(status_code=401, detail="Token inválido")

# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Adventure Game Web Interface API",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": str(datetime.now() - system_manager.system_stats["uptime"]).split('.')[0]
    }

@app.get("/api/metrics")
async def get_metrics(current_user: dict = Depends(get_current_user)):
    """Obtiene métricas del sistema"""
    return await system_manager.get_system_metrics()

@app.get("/api/system/status")
async def get_system_status(current_user: dict = Depends(get_current_user)):
    """Estado detallado del sistema"""
    return {
        "adventure_game": {
            "status": "running" if system_manager.memory_system else "stopped",
            "memory_system": system_manager.memory_system is not None,
            "mcp_provider": system_manager.mcp_provider is not None
        },
        "backup_system": {
            "status": "running" if system_manager.backup_manager else "stopped",
            "manager": system_manager.backup_manager is not None,
            "restore": system_manager.restore_manager is not None
        },
        "websockets": {
            "active_connections": len(system_manager.websocket_manager.active_connections)
        }
    }

@app.get("/api/backups")
async def list_backups(current_user: dict = Depends(get_current_user)):
    """Lista todos los backups disponibles"""
    if not system_manager.backup_manager:
        raise HTTPException(status_code=503, detail="Sistema de backup no disponible")
    
    backups = system_manager.backup_manager.list_backups()
    return [
        {
            "backup_id": backup.backup_id,
            "timestamp": backup.timestamp.isoformat(),
            "size_bytes": backup.size_bytes,
            "files_count": backup.files_count,
            "backup_type": backup.backup_type,
            "integrity_hash": backup.integrity_hash[:16] + "...",
            "game_state_summary": backup.game_state_summary
        }
        for backup in backups
    ]

@app.post("/api/backups/create")
async def create_backup(
    backup_type: str = "manual",
    current_user: dict = Depends(get_current_user)
):
    """Crea un nuevo backup"""
    if not system_manager.backup_manager:
        raise HTTPException(status_code=503, detail="Sistema de backup no disponible")
    
    backup_id = system_manager.backup_manager.create_backup(backup_type)
    
    if backup_id:
        # Notificar por WebSocket
        await system_manager.websocket_manager.broadcast({
            "type": "backup_created",
            "backup_id": backup_id,
            "timestamp": datetime.now().isoformat()
        })
        
        return {"success": True, "backup_id": backup_id}
    else:
        raise HTTPException(status_code=500, detail="Error creando backup")

@app.get("/api/events")
async def get_events(
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Obtiene eventos del sistema de memoria"""
    if not system_manager.memory_system:
        raise HTTPException(status_code=503, detail="Sistema de memoria no disponible")
    
    try:
        # Obtener eventos directamente de la base de datos
        cursor = system_manager.memory_system.db_connection.execute(
            "SELECT * FROM game_events ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        events = [dict(row) for row in cursor.fetchall()]
        
        return {
            "events": events,
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS MULTI-JUGADOR
# ============================================================================

@app.get("/api/multiplayer/status")
async def get_multiplayer_status(current_user: dict = Depends(get_current_user)):
    """Estado del sistema multi-jugador"""
    if not MULTIPLAYER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Sistema multi-jugador no disponible")
    
    return websocket_manager.get_connection_stats()

@app.get("/api/multiplayer/players")
async def get_active_players(current_user: dict = Depends(get_current_user)):
    """Lista de jugadores activos"""
    if not MULTIPLAYER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Sistema multi-jugador no disponible")
    
    multiplayer_game = get_multiplayer_game()
    players = multiplayer_game.session_manager.get_all_players()
    
    return {
        "players": [player.to_dict() for player in players],
        "total": len(players),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/multiplayer/broadcast")
async def broadcast_message(
    message: str,
    message_type: str = "admin_announcement",
    current_user: dict = Depends(get_current_user)
):
    """Envía mensaje broadcast a todos los jugadores"""
    if not MULTIPLAYER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Sistema multi-jugador no disponible")
    
    broadcast_data = {
        "type": message_type,
        "message": message,
        "from": "admin",
        "timestamp": datetime.now().isoformat()
    }
    
    await websocket_manager.broadcast_to_all(broadcast_data)
    
    return {"success": True, "message": "Mensaje enviado a todos los jugadores"}

@app.delete("/api/multiplayer/players/{player_id}")
async def disconnect_player(
    player_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Desconecta un jugador específico"""
    if not MULTIPLAYER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Sistema multi-jugador no disponible")
    
    try:
        await websocket_manager.disconnect_player(player_id)
        return {"success": True, "message": f"Jugador {player_id} desconectado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/multiplayer")
async def websocket_multiplayer_endpoint(websocket: WebSocket):
    """WebSocket principal para multi-jugador"""
    if not MULTIPLAYER_AVAILABLE:
        await websocket.close(code=4503, reason="Sistema multi-jugador no disponible")
        return
    
    await websocket_endpoint(websocket)

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
        await websocket.send_text(json.dumps(initial_data))
        
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

# Servir archivos estáticos del frontend si existe
if FRONTEND_BUILD_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_BUILD_DIR / "static")), name="static")

if __name__ == "__main__":
    print("🌐 ADVENTURE GAME WEB INTERFACE")
    print("=" * 50)
    print("🚀 Iniciando servidor backend...")
    print("📊 Dashboard: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
