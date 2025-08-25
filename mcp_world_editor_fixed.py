#!/usr/bin/env python3
"""
🌍 MCP WORLD EDITOR - Editor de Mundos aprovechando Model Context Protocol
Interfaz estandarizada para crear lugares, objetos y eventos usando la infraestructura existente

Integra con:
- memory_system.py (para persistencia)
- mcp_integration.py (para contexto inteligente)
- ai_engine.py (para validación con IA)
"""

import asyncio
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

# Imports del sistema existente
from memory_system import PerfectMemorySystem, Location, GameObject
from mcp_integration import MCPContextProvider

class MCPWorldEditor:
    """
    Editor de mundos que aprovecha el protocolo MCP para crear contenido inteligente
    """
    
    def __init__(self, memory_system: PerfectMemorySystem = None, mcp_provider: MCPContextProvider = None, db_path: str = "adventure_world.db"):
        self.db_path = db_path
        self.memory_system = memory_system
        self.mcp_provider = mcp_provider
        self.templates_cache = {}
        
        # Inicializar sistemas si no se proporcionaron
        if self.memory_system is None:
            self.memory_system = PerfectMemorySystem()
        if self.mcp_provider is None:
            self.mcp_provider = MCPContextProvider(self.memory_system)
        
        # Predefined templates
        self.location_presets = {
            "forest": {
                "atmosphere": "natural y tranquilo",
                "lighting": "filtered",
                "properties": {"nature": True, "sounds": "birds_wind"}
            },
            "dungeon": {
                "atmosphere": "oscuro y amenazante", 
                "lighting": "dark",
                "properties": {"dangerous": True, "echo": True}
            },
            "castle": {
                "atmosphere": "majestuoso y antiguo",
                "lighting": "dim",
                "properties": {"historic": True, "stone_walls": True}
            },
            "shop": {
                "atmosphere": "acogedor y comercial",
                "lighting": "bright", 
                "properties": {"commerce": True, "safe": True}
            }
        }
        
        self.object_presets = {
            "weapon": {
                "properties": {"damage": 10, "durability": 100, "type": "weapon"},
                "keywords": ["arma", "combate", "weapon"],
                "is_takeable": True,
                "is_usable": True
            },
            "tool": {
                "properties": {"durability": 100, "type": "tool"},
                "keywords": ["herramienta", "tool", "útil"],
                "is_takeable": True,
                "is_usable": True
            },
            "treasure": {
                "properties": {"value": 100, "type": "treasure"},
                "keywords": ["tesoro", "valioso", "treasure"],
                "is_takeable": True,
                "is_usable": False
            },
            "furniture": {
                "properties": {"type": "furniture"},
                "keywords": ["mueble", "furniture"],
                "is_takeable": False,
                "is_usable": True
            }
        }
    
    async def initialize(self) -> bool:
        """Inicializa el editor con conexión a sistemas existentes"""
        try:
            # Solo inicializar si los sistemas no fueron proporcionados en el constructor
            if not hasattr(self.memory_system, 'initialized') or not self.memory_system.initialized:
                await self.memory_system.initialize()
            
            print("✅ MCP World Editor inicializado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando editor: {e}")
            return False

    # =============================================================================
    # MÉTODOS PARA WEB API - INTERFAZ SIMPLE
    # =============================================================================
    
    async def create_location_with_mcp(self, name: str, description: str, preset: str = None, 
                                      connections: List[str] = None, properties: Dict = None) -> Dict[str, Any]:
        """Crear ubicación desde parámetros directos (API web)"""
        try:
            # Preparar propiedades
            final_properties = properties or {}
            
            # Aplicar preset si se especifica
            if preset and preset in self.location_presets:
                preset_data = self.location_presets[preset]
                final_properties.update(preset_data.get("properties", {}))
                final_properties["atmosphere"] = preset_data.get("atmosphere", "")
                final_properties["lighting"] = preset_data.get("lighting", "normal")
            
            # Crear ubicación usando el sistema existente
            location_id = await self.memory_system.create_location(
                name=name,
                description=description,
                connections={conn: conn for conn in (connections or [])},
                properties=final_properties
            )
            
            return {
                "success": True,
                "location_id": location_id,
                "name": name,
                "description": description,
                "preset": preset,
                "properties": final_properties
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_object_with_mcp(self, name: str, description: str, location_name: str, 
                                    preset: str = None, properties: Dict = None) -> Dict[str, Any]:
        """Crear objeto desde parámetros directos (API web)"""
        try:
            # Preparar propiedades
            final_properties = properties or {}
            
            # Aplicar preset si se especifica
            if preset and preset in self.object_presets:
                preset_data = self.object_presets[preset]
                final_properties.update(preset_data.get("properties", {}))
            
            # Crear objeto usando el sistema existente
            object_id = await self.memory_system.create_object(
                name=name,
                description=description,
                location_name=location_name,
                properties=final_properties
            )
            
            return {
                "success": True,
                "object_id": object_id,
                "name": name,
                "description": description,
                "location_name": location_name,
                "preset": preset,
                "properties": final_properties
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_event_with_mcp(self, name: str, description: str, trigger_type: str,
                                   trigger_value: str, action_type: str, action_data: Dict = None,
                                   properties: Dict = None) -> Dict[str, Any]:
        """Crear evento desde parámetros directos (API web)"""
        try:
            # Crear evento en base de datos personalizada
            event_id = str(uuid.uuid4())
            
            # Simular creación de evento (el sistema original no tiene eventos nativos)
            event_data = {
                "id": event_id,
                "name": name,
                "description": description,
                "trigger_type": trigger_type,
                "trigger_value": trigger_value,
                "action_type": action_type,
                "action_data": action_data or {},
                "properties": properties or {},
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "event_id": event_id,
                "name": name,
                "description": description,
                "trigger_type": trigger_type,
                "action_type": action_type
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_world_overview_with_mcp(self) -> Dict[str, Any]:
        """Vista general del mundo con estadísticas"""
        try:
            # Obtener datos del sistema de memoria
            locations = self.memory_system.get_all_locations()
            objects = self.memory_system.get_all_objects()
            
            return {
                "total_locations": len(locations),
                "total_objects": len(objects),
                "total_events": 0,  # Los eventos no están implementados nativamente
                "locations": [
                    {
                        "name": loc.name,
                        "description": loc.description,
                        "connections": list(loc.connections.keys()) if loc.connections else []
                    }
                    for loc in locations
                ],
                "objects": [
                    {
                        "name": obj.name,
                        "description": obj.description,
                        "location_name": obj.location_name
                    }
                    for obj in objects
                ],
                "events": [],
                "mcp_stats": {
                    "total_locations": len(locations),
                    "total_objects": len(objects),
                    "total_events": 0
                }
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "total_locations": 0,
                "total_objects": 0,
                "total_events": 0
            }
    
    def export_templates_to_json(self) -> Dict[str, Any]:
        """Exportar templates y configuración"""
        return {
            "location_presets": self.location_presets,
            "object_presets": self.object_presets,
            "templates_cache": self.templates_cache,
            "exported_at": datetime.now().isoformat()
        }
    
    async def load_templates_from_json(self, templates_data: Dict) -> Dict[str, Any]:
        """Importar templates desde JSON"""
        try:
            if "location_presets" in templates_data:
                self.location_presets.update(templates_data["location_presets"])
            
            if "object_presets" in templates_data:
                self.object_presets.update(templates_data["object_presets"])
            
            return {
                "success": True,
                "message": "Templates importados exitosamente"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def quick_location(self, name: str, theme: str = "generic", connections: List[str] = None) -> Dict[str, Any]:
        """Creación rápida de ubicación con tema automático"""
        try:
            preset = "forest" if theme == "nature" else theme if theme in self.location_presets else "forest"
            
            description = f"Una {theme} llamada {name}"
            if theme == "forest" or theme == "nature":
                description = f"Un hermoso bosque conocido como {name}"
            elif theme == "castle":
                description = f"Un majestuoso castillo llamado {name}"
            elif theme == "dungeon":
                description = f"Una misteriosa mazmorra conocida como {name}"
            elif theme == "shop":
                description = f"Una acogedora tienda llamada {name}"
            
            return await self.create_location_with_mcp(
                name=name,
                description=description,
                preset=preset,
                connections=connections or []
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# =============================================================================
# DEMO Y TESTING
# =============================================================================

async def demo_mcp_world_editor():
    """Demostración del editor MCP"""
    print("🌍 Demo MCP World Editor")
    print("=" * 50)
    
    editor = MCPWorldEditor()
    await editor.initialize()
    
    # Crear ubicación de prueba
    result = await editor.create_location_with_mcp(
        name="Bosque Encantado",
        description="Un bosque mágico lleno de misterios",
        preset="forest",
        connections=["Ciudad Principal"]
    )
    
    if result["success"]:
        print(f"✅ Ubicación creada: {result['location_id']}")
    
    # Crear objeto de prueba
    result = await editor.create_object_with_mcp(
        name="Seta Luminosa",
        description="Una seta que brilla con luz propia",
        location_name="Bosque Encantado",
        preset="treasure"
    )
    
    if result["success"]:
        print(f"✅ Objeto creado: {result['object_id']}")
    
    # Vista general
    overview = await editor.get_world_overview_with_mcp()
    print(f"\n📊 Resumen: {overview['total_locations']} ubicaciones, {overview['total_objects']} objetos")

if __name__ == "__main__":
    asyncio.run(demo_mcp_world_editor())
