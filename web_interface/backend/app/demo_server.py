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
# -----------------------------
# Almacenamiento en memoria (Demo)
# -----------------------------
locations_db = [
    {"id": 1, "name": "Torre Principal", "description": "Una torre majestuosa", "preset": "castle"},
    {"id": 2, "name": "Patio del Castillo", "description": "Un patio amplio", "preset": "castle"},
    {"id": 3, "name": "Biblioteca Mágica", "description": "Libros antiguos y magia", "preset": "dungeon"}
]
objects_db = [
    {"id": 1, "name": "Espada Brillante", "description": "Brilla con luz propia", "location_name": "Torre Principal", "preset": "weapon"},
    {"id": 2, "name": "Orbe de Poder", "description": "Pulsa con energía", "location_name": "Torre Principal", "preset": "treasure"}
]
events_db = [
    {"id": 1, "name": "Bienvenida Real", "trigger_type": "location_enter", "trigger_value": "Torre Principal", "action_type": "message"}
]
def get_next_id(db):
    return max([item["id"] for item in db], default=0) + 1

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
        "total_locations": len(locations_db),
        "total_objects": len(objects_db),
        "total_events": len(events_db),
        "locations": locations_db,
        "objects": objects_db,
        "events": events_db
    }

@app.post("/api/mcp/locations")
async def create_location_mcp(location_data: dict):
    """Crear ubicación (Demo)"""
    new_location = {
        "id": get_next_id(locations_db),
        "name": location_data.get("name", "Nueva Ubicación"),
        "description": location_data.get("description", "Descripción generada"),
        "preset": location_data.get("preset", "forest"),
        "created_at": datetime.now().isoformat()
    }
    locations_db.append(new_location)
    return {"success": True, "message": "Ubicación creada exitosamente", "location": new_location}

@app.post("/api/mcp/objects")
async def create_object_mcp(object_data: dict):
    """Crear objeto (Demo)"""
    new_object = {
        "id": get_next_id(objects_db),
        "name": object_data.get("name", "Nuevo Objeto"),
        "description": object_data.get("description", "Descripción generada"),
        "location_name": object_data.get("location_name", "Ubicación desconocida"),
        "preset": object_data.get("preset", "treasure"),
        "created_at": datetime.now().isoformat()
    }
    objects_db.append(new_object)
    return {"success": True, "message": "Objeto creado exitosamente", "object": new_object}

@app.post("/api/mcp/events")
async def create_event_mcp(event_data: dict):
    """Crear evento (Demo)"""
    new_event = {
        "id": get_next_id(events_db),
        "name": event_data.get("name", "Nuevo Evento"),
        "description": event_data.get("description", "Descripción generada"),
        "trigger_type": event_data.get("trigger_type", "location_enter"),
        "trigger_value": event_data.get("trigger_value", ""),
        "action_type": event_data.get("action_type", "message"),
        "created_at": datetime.now().isoformat()
    }
    events_db.append(new_event)
    return {"success": True, "message": "Evento creado exitosamente", "event": new_event}

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
# -----------------------------
# ABM: Editar y Eliminar (PUT/DELETE)
# -----------------------------
from fastapi import HTTPException

# Editar ubicación
@app.put("/api/mcp/locations/{location_id}")
async def update_location(location_id: int, location_data: dict):
    for loc in locations_db:
        if loc["id"] == location_id:
            loc.update({
                "name": location_data.get("name", loc["name"]),
                "description": location_data.get("description", loc["description"]),
                "preset": location_data.get("preset", loc["preset"])
            })
            return {"success": True, "message": "Ubicación actualizada", "location": loc}
    raise HTTPException(status_code=404, detail="Ubicación no encontrada")

# Eliminar ubicación
@app.delete("/api/mcp/locations/{location_id}")
async def delete_location(location_id: int):
    for loc in locations_db:
        if loc["id"] == location_id:
            locations_db.remove(loc)
            return {"success": True, "message": "Ubicación eliminada"}
    raise HTTPException(status_code=404, detail="Ubicación no encontrada")

# Editar objeto
@app.put("/api/mcp/objects/{object_id}")
async def update_object(object_id: int, object_data: dict):
    for obj in objects_db:
        if obj["id"] == object_id:
            obj.update({
                "name": object_data.get("name", obj["name"]),
                "description": object_data.get("description", obj["description"]),
                "location_name": object_data.get("location_name", obj["location_name"]),
                "preset": object_data.get("preset", obj["preset"])
            })
            return {"success": True, "message": "Objeto actualizado", "object": obj}
    raise HTTPException(status_code=404, detail="Objeto no encontrado")

# Eliminar objeto
@app.delete("/api/mcp/objects/{object_id}")
async def delete_object(object_id: int):
    for obj in objects_db:
        if obj["id"] == object_id:
            objects_db.remove(obj)
            return {"success": True, "message": "Objeto eliminado"}
    raise HTTPException(status_code=404, detail="Objeto no encontrado")

# Editar evento
@app.put("/api/mcp/events/{event_id}")
async def update_event(event_id: int, event_data: dict):
    for ev in events_db:
        if ev["id"] == event_id:
            ev.update({
                "name": event_data.get("name", ev["name"]),
                "description": event_data.get("description", ev["description"]),
                "trigger_type": event_data.get("trigger_type", ev["trigger_type"]),
                "trigger_value": event_data.get("trigger_value", ev["trigger_value"]),
                "action_type": event_data.get("action_type", ev["action_type"])
            })
            return {"success": True, "message": "Evento actualizado", "event": ev}
    raise HTTPException(status_code=404, detail="Evento no encontrado")

# Eliminar evento
@app.delete("/api/mcp/events/{event_id}")
async def delete_event(event_id: int):
    for ev in events_db:
        if ev["id"] == event_id:
            events_db.remove(ev)
            return {"success": True, "message": "Evento eliminado"}
    raise HTTPException(status_code=404, detail="Evento no encontrado")

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
