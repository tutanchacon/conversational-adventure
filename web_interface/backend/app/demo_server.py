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

@app.get("/api/system/status")
async def system_status():
    """Estado del sistema (Demo)"""
    return {
        "status": "running",
        "uptime": "demo",
        "requests_count": 42,
        "active_sessions": 1,
        "last_backup": "2025-08-23T19:44:53",
        "system_health": "healthy"
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

# =============================================================================
# 🌍 MCP WORLD EDITOR ENDPOINTS (DEMO)
# =============================================================================

@app.get("/api/mcp/status")
async def get_mcp_status():
    """Estado del MCP World Editor (Demo)"""
    return {
        "status": "available",
        "features": {
            "location_creation": True,
            "object_creation": True,
            "event_creation": True,
            "template_system": True,
            "json_export": True
        },
        "presets": {
            "locations": ["forest", "dungeon", "castle", "shop"],
            "objects": ["weapon", "tool", "treasure", "furniture"],
            "events": ["location_enter", "object_use", "command", "time"]
        }
    }

@app.get("/api/mcp/world/overview")
async def get_world_overview():
    """Vista general del mundo (Demo)"""
    return {
        "total_locations": 3,
        "total_objects": 5,
        "total_events": 2,
        "locations": [
            {"name": "Torre Principal", "description": "Una torre majestuosa con vistas al reino", "connections": ["Patio del Castillo"]},
            {"name": "Patio del Castillo", "description": "Un amplio patio con jardines bien cuidados", "connections": ["Torre Principal", "Biblioteca Mágica"]},
            {"name": "Biblioteca Mágica", "description": "Una biblioteca llena de libros antiguos y pergaminos mágicos", "connections": ["Patio del Castillo"]}
        ],
        "objects": [
            {"name": "Espada Brillante", "description": "Una espada que brilla con luz propia", "location_name": "Torre Principal"},
            {"name": "Orbe de Poder", "description": "Un orbe mágico que pulsa con energía", "location_name": "Torre Principal"},
            {"name": "Fuente Mágica", "description": "Una fuente que nunca se agota", "location_name": "Patio del Castillo"},
            {"name": "Libro de Hechizos", "description": "Un grimorio con hechizos poderosos", "location_name": "Biblioteca Mágica"},
            {"name": "Mesa de Lectura", "description": "Una mesa de madera tallada para estudiar", "location_name": "Biblioteca Mágica"}
        ],
        "events": [
            {"name": "Bienvenida Real", "trigger_type": "location_enter", "trigger_value": "Torre Principal", "action_type": "message"},
            {"name": "Sabiduría Antigua", "trigger_type": "object_use", "trigger_value": "Libro de Hechizos", "action_type": "message"}
        ]
    }

@app.post("/api/mcp/locations")
async def create_location_mcp(location_data: dict):
    """Crear ubicación (Demo)"""
    return {
        "success": True,
        "message": "Ubicación creada exitosamente (Demo)",
        "location": {
            "name": location_data.get("name", "Nueva Ubicación"),
            "description": location_data.get("description", "Descripción generada"),
            "preset": location_data.get("preset", "forest"),
            "created_at": datetime.now().isoformat()
        }
    }

@app.post("/api/mcp/objects")
async def create_object_mcp(object_data: dict):
    """Crear objeto (Demo)"""
    return {
        "success": True,
        "message": "Objeto creado exitosamente (Demo)",
        "object": {
            "name": object_data.get("name", "Nuevo Objeto"),
            "description": object_data.get("description", "Descripción generada"),
            "location_name": object_data.get("location_name", "Ubicación desconocida"),
            "preset": object_data.get("preset", "treasure"),
            "created_at": datetime.now().isoformat()
        }
    }

@app.post("/api/mcp/events")
async def create_event_mcp(event_data: dict):
    """Crear evento (Demo)"""
    return {
        "success": True,
        "message": "Evento creado exitosamente (Demo)",
        "event": {
            "name": event_data.get("name", "Nuevo Evento"),
            "description": event_data.get("description", "Descripción generada"),
            "trigger_type": event_data.get("trigger_type", "location_enter"),
            "trigger_value": event_data.get("trigger_value", ""),
            "action_type": event_data.get("action_type", "message"),
            "created_at": datetime.now().isoformat()
        }
    }

@app.get("/api/mcp/templates/export")
async def export_templates():
    """Exportar templates (Demo)"""
    return {
        "success": True,
        "templates": {
            "locations": ["forest", "castle", "dungeon", "shop"],
            "objects": ["weapon", "tool", "treasure", "furniture"],
            "events": ["location_enter", "object_use", "command", "time"]
        },
        "exported_at": datetime.now().isoformat()
    }

@app.post("/api/mcp/templates/import")
async def import_templates(templates_data: dict):
    """Importar templates (Demo)"""
    return {
        "success": True,
        "message": "Templates importados exitosamente (Demo)",
        "imported_at": datetime.now().isoformat()
    }

@app.post("/api/mcp/quick/location")
async def quick_create_location(quick_data: dict):
    """Creación rápida de ubicación (Demo)"""
    return {
        "success": True,
        "message": "Ubicación rápida creada exitosamente (Demo)",
        "location": {
            "name": quick_data.get("name", "Ubicación Rápida"),
            "theme": quick_data.get("theme", "generic"),
            "created_at": datetime.now().isoformat()
        }
    }

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
