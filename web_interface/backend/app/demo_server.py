"""
🚀 DEMO RÁPIDO - Adventure Game Web Interface
Backend demo simplificado que funciona en puerto 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import json

# Crear aplicación FastAPI
app = FastAPI(
    title="Adventure Game Web Interface",
    description="Demo del panel de administración",
    version="2.0.0-demo"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "🎮 Adventure Game Web Interface",
        "version": "2.0.0-demo",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "✅ API REST funcionando",
            "✅ Documentación automática",
            "✅ CORS configurado",
            "🔄 WebSocket (próximamente)",
            "🔐 Autenticación JWT (próximamente)"
        ]
    }

@app.get("/api/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Sistema funcionando correctamente"
    }

@app.get("/api/demo/metrics")
async def demo_metrics():
    """Métricas demo"""
    return {
        "uptime": "2h 15m 30s",
        "requests_count": 142,
        "active_sessions": 3,
        "system_health": "excellent",
        "backup_count": 2,
        "events_count": 1234,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/demo/backups")
async def demo_backups():
    """Lista de backups demo"""
    return [
        {
            "backup_id": "backup_20250823_194635",
            "timestamp": "2025-08-23T19:46:35",
            "size_bytes": 109408,
            "files_count": 37,
            "backup_type": "professional_v1.1.0",
            "status": "completed"
        },
        {
            "backup_id": "backup_20250823_194453",
            "timestamp": "2025-08-23T19:44:53", 
            "size_bytes": 107928,
            "files_count": 36,
            "backup_type": "test",
            "status": "completed"
        }
    ]

if __name__ == "__main__":
    print("🎮 ADVENTURE GAME WEB INTERFACE - DEMO")
    print("=" * 50)
    print("🚀 Servidor demo iniciando en puerto 8001...")
    print("📊 Dashboard: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    print("🧪 Métricas: http://localhost:8001/api/demo/metrics")
    print("💾 Backups: http://localhost:8001/api/demo/backups")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
