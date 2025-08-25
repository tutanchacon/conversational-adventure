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

@dataclass
class WorldEditorTemplate:
    """Template base para elementos del mundo"""
    id: str
    name: str
    description: str
    created_at: str = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

@dataclass
class LocationTemplate(WorldEditorTemplate):
    """Template para ubicaciones con validación MCP"""
    connections: Dict[str, str] = None
    properties: Dict[str, Any] = None
    atmosphere: str = ""
    lighting: str = "normal"
    size: str = "medium"
    theme: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        if self.connections is None:
            self.connections = {}
        if self.properties is None:
            self.properties = {}

@dataclass 
class ObjectTemplate(WorldEditorTemplate):
    """Template para objetos con contexto MCP"""
    location_id: str = ""
    properties: Dict[str, Any] = None
    is_takeable: bool = True
    is_usable: bool = False
    is_hidden: bool = False
    keywords: List[str] = None
    ai_context: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        if self.properties is None:
            self.properties = {}
        if self.keywords is None:
            self.keywords = []

@dataclass
class EventTemplate(WorldEditorTemplate):
    """Template para eventos con triggers MCP"""
    trigger_type: str = "location_enter"  # location_enter, object_use, command, time
    trigger_condition: str = ""
    action_type: str = "message"  # message, spawn_object, modify_object, change_location
    action_data: Dict[str, Any] = None
    is_repeatable: bool = False
    cooldown_seconds: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        if self.action_data is None:
            self.action_data = {}

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
            if self.memory_system is None:
                self.memory_system = PerfectMemorySystem(self.db_path)
                await self.memory_system.initialize()
            
            if self.mcp_provider is None:
                self.mcp_provider = MCPContextProvider(self.memory_system)
            
            print("✅ MCP World Editor inicializado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando editor: {e}")
            return False
    
    async def create_location_with_mcp(self, template: LocationTemplate, 
                                     ai_enhance: bool = True) -> Tuple[bool, str]:
        """
        Crea una ubicación usando template y contexto MCP
        """
        try:
            # Validar template
            validation_result = await self._validate_location_template(template)
            if not validation_result["valid"]:
                return False, f"Template inválido: {validation_result['reason']}"
            
            # Enriquecer con contexto MCP si se solicita
            if ai_enhance:
                template = await self._enhance_location_with_mcp(template)
            
            # Crear ubicación usando el sistema existente
            location = await self.memory_system.create_location(
                name=template.name,
                description=template.description,
                connections=template.connections,
                properties={
                    **template.properties,
                    "atmosphere": template.atmosphere,
                    "lighting": template.lighting,
                    "size": template.size,
                    "theme": template.theme,
                    "created_by": "mcp_editor",
                    "editor_metadata": template.metadata
                }
            )
            
            # Actualizar template con ID real
            template.id = location.id
            
            # Cache del template para referencia
            self.templates_cache[location.id] = template
            
            print(f"✅ Ubicación creada con MCP: {template.name} ({location.id})")
            return True, location.id
            
        except Exception as e:
            print(f"❌ Error creando ubicación: {e}")
            return False, str(e)
    
    async def create_object_with_mcp(self, template: ObjectTemplate,
                                   ai_enhance: bool = True) -> Tuple[bool, str]:
        """
        Crea un objeto usando template y contexto MCP
        """
        try:
            # Validar template
            validation_result = await self._validate_object_template(template)
            if not validation_result["valid"]:
                return False, f"Template inválido: {validation_result['reason']}"
            
            # Enriquecer con contexto MCP
            if ai_enhance:
                template = await self._enhance_object_with_mcp(template)
            
            # Crear objeto usando el sistema existente
            game_object = await self.memory_system.create_object(
                name=template.name,
                description=template.description,
                location_id=template.location_id,
                properties={
                    **template.properties,
                    "is_takeable": template.is_takeable,
                    "is_usable": template.is_usable,
                    "is_hidden": template.is_hidden,
                    "keywords": template.keywords,
                    "ai_context": template.ai_context,
                    "created_by": "mcp_editor",
                    "editor_metadata": template.metadata
                }
            )
            
            # Actualizar template con ID real
            template.id = game_object.id
            
            # Cache del template
            self.templates_cache[game_object.id] = template
            
            print(f"✅ Objeto creado con MCP: {template.name} ({game_object.id})")
            return True, game_object.id
            
        except Exception as e:
            print(f"❌ Error creando objeto: {e}")
            return False, str(e)
    
    async def create_event_with_mcp(self, template: EventTemplate) -> Tuple[bool, str]:
        """
        Crea un evento usando template MCP
        Nota: Los eventos se almacenan en una tabla separada para triggers
        """
        try:
            # Validar template
            validation_result = await self._validate_event_template(template)
            if not validation_result["valid"]:
                return False, f"Template inválido: {validation_result['reason']}"
            
            # Crear tabla de eventos personalizados si no existe
            await self._ensure_custom_events_table()
            
            # Generar ID único
            event_id = str(uuid.uuid4())
            template.id = event_id
            
            # Insertar evento en tabla personalizada
            cursor = self.memory_system.db_connection.execute("""
                INSERT INTO custom_events 
                (id, name, description, trigger_type, trigger_condition, 
                 action_type, action_data, is_repeatable, cooldown_seconds, 
                 created_at, metadata, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                event_id,
                template.name,
                template.description,
                template.trigger_type,
                template.trigger_condition,
                template.action_type,
                json.dumps(template.action_data),
                template.is_repeatable,
                template.cooldown_seconds,
                template.created_at,
                json.dumps(template.metadata)
            ))
            
            # Registrar en el sistema de eventos principal
            await self.memory_system._record_event(
                event_type="custom_event_created",
                actor="mcp_editor",
                action=f"created custom event '{template.name}'",
                target=event_id,
                location_id=template.action_data.get("location_id", "global"),
                context={"event_template": asdict(template)}
            )
            
            self.templates_cache[event_id] = template
            
            print(f"✅ Evento creado con MCP: {template.name} ({event_id})")
            return True, event_id
            
        except Exception as e:
            print(f"❌ Error creando evento: {e}")
            return False, str(e)
    
    async def _validate_location_template(self, template: LocationTemplate) -> Dict[str, Any]:
        """Valida un template de ubicación usando contexto MCP"""
        
        # Validaciones básicas
        if not template.name or len(template.name.strip()) < 3:
            return {"valid": False, "reason": "Nombre debe tener al menos 3 caracteres"}
        
        if not template.description or len(template.description.strip()) < 10:
            return {"valid": False, "reason": "Descripción debe tener al menos 10 caracteres"}
        
        # Validar conexiones contra ubicaciones existentes
        if template.connections:
            for direction, target_id in template.connections.items():
                if target_id == template.id:
                    return {"valid": False, "reason": f"No puede conectar consigo misma en {direction}"}
                
                # Verificar que la ubicación destino existe
                existing_locations = await self._get_existing_location_ids()
                if target_id not in existing_locations:
                    print(f"⚠️ Advertencia: {target_id} no existe aún, pero se permitirá para creación en lotes")
        
        return {"valid": True, "reason": "Template válido"}
    
    async def _validate_object_template(self, template: ObjectTemplate) -> Dict[str, Any]:
        """Valida un template de objeto usando contexto MCP"""
        
        # Validaciones básicas
        if not template.name or len(template.name.strip()) < 2:
            return {"valid": False, "reason": "Nombre debe tener al menos 2 caracteres"}
        
        if not template.description or len(template.description.strip()) < 5:
            return {"valid": False, "reason": "Descripción debe tener al menos 5 caracteres"}
        
        # Validar ubicación destino
        if template.location_id:
            existing_locations = await self._get_existing_location_ids()
            if template.location_id not in existing_locations:
                return {"valid": False, "reason": f"Ubicación {template.location_id} no existe"}
        
        return {"valid": True, "reason": "Template válido"}
    
    async def _validate_event_template(self, template: EventTemplate) -> Dict[str, Any]:
        """Valida un template de evento"""
        
        valid_triggers = ["location_enter", "object_use", "command", "time"]
        valid_actions = ["message", "spawn_object", "modify_object", "change_location"]
        
        if template.trigger_type not in valid_triggers:
            return {"valid": False, "reason": f"Trigger inválido: {template.trigger_type}"}
        
        if template.action_type not in valid_actions:
            return {"valid": False, "reason": f"Acción inválida: {template.action_type}"}
        
        if not template.trigger_condition:
            return {"valid": False, "reason": "Condición de trigger requerida"}
        
        return {"valid": True, "reason": "Template válido"}
    
    async def _enhance_location_with_mcp(self, template: LocationTemplate) -> LocationTemplate:
        """Enriquece una ubicación usando contexto MCP"""
        
        # Si hay ubicaciones cercanas, obtener contexto
        if template.connections:
            nearby_context = []
            for direction, target_id in template.connections.items():
                try:
                    context = await self.mcp_provider.get_location_context(target_id)
                    nearby_context.append({
                        "direction": direction,
                        "target": target_id,
                        "objects_count": context.get("object_count", 0)
                    })
                except:
                    pass  # Ubicación destino no existe aún
            
            # Añadir contexto de ubicaciones cercanas
            template.metadata["nearby_locations"] = nearby_context
        
        # Enriquecer propiedades basadas en preset
        if template.theme and template.theme in self.location_presets:
            preset = self.location_presets[template.theme]
            for key, value in preset.items():
                if key == "properties":
                    template.properties.update(value)
                else:
                    setattr(template, key, value)
        
        return template
    
    async def _enhance_object_with_mcp(self, template: ObjectTemplate) -> ObjectTemplate:
        """Enriquece un objeto usando contexto MCP"""
        
        # Obtener contexto de la ubicación donde se colocará
        if template.location_id:
            try:
                location_context = await self.mcp_provider.get_location_context(template.location_id)
                
                # Sugerir keywords basadas en objetos existentes
                existing_objects = location_context.get("objects_present", [])
                if existing_objects:
                    # Extraer keywords comunes
                    common_themes = set()
                    for obj in existing_objects:
                        obj_props = obj.get("properties", {})
                        if "type" in obj_props:
                            common_themes.add(obj_props["type"])
                    
                    template.metadata["location_themes"] = list(common_themes)
                
                template.metadata["location_object_count"] = len(existing_objects)
                
            except Exception as e:
                print(f"⚠️ No se pudo obtener contexto de ubicación: {e}")
        
        # Aplicar preset si corresponde
        for preset_name, preset_data in self.object_presets.items():
            if preset_name in template.name.lower() or preset_name in template.description.lower():
                for key, value in preset_data.items():
                    if key == "properties":
                        template.properties.update(value)
                    elif key == "keywords":
                        template.keywords.extend([k for k in value if k not in template.keywords])
                    else:
                        setattr(template, key, value)
                break
        
        return template
    
    async def _get_existing_location_ids(self) -> List[str]:
        """Obtiene IDs de ubicaciones existentes"""
        cursor = self.memory_system.db_connection.execute("SELECT id FROM locations")
        return [row[0] for row in cursor.fetchall()]
    
    async def _ensure_custom_events_table(self):
        """Asegura que la tabla de eventos personalizados existe"""
        self.memory_system.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS custom_events (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                trigger_type TEXT NOT NULL,
                trigger_condition TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action_data TEXT NOT NULL,
                is_repeatable BOOLEAN DEFAULT 0,
                cooldown_seconds INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                metadata TEXT,
                is_active BOOLEAN DEFAULT 1,
                times_triggered INTEGER DEFAULT 0,
                last_triggered TEXT
            )
        """)
        self.memory_system.db_connection.commit()
    
    async def export_templates_to_json(self, filename: str = None) -> str:
        """Exporta todos los templates creados a JSON"""
        if filename is None:
            filename = f"mcp_world_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "editor_version": "1.0.0",
                "mcp_enabled": True,
                "total_templates": len(self.templates_cache)
            },
            "templates": {
                template_id: asdict(template) 
                for template_id, template in self.templates_cache.items()
            },
            "presets": {
                "locations": self.location_presets,
                "objects": self.object_presets
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Templates exportados a: {filename}")
        return filename
    
    async def load_templates_from_json(self, filename: str) -> bool:
        """Carga templates desde JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            templates = data.get("templates", {})
            created_count = 0
            
            for template_id, template_data in templates.items():
                # Determinar tipo de template basado en campos
                if "connections" in template_data:
                    # Es una ubicación
                    template = LocationTemplate(**template_data)
                    success, result_id = await self.create_location_with_mcp(template, ai_enhance=False)
                elif "location_id" in template_data:
                    # Es un objeto
                    template = ObjectTemplate(**template_data)
                    success, result_id = await self.create_object_with_mcp(template, ai_enhance=False)
                elif "trigger_type" in template_data:
                    # Es un evento
                    template = EventTemplate(**template_data)
                    success, result_id = await self.create_event_with_mcp(template)
                else:
                    print(f"⚠️ Template desconocido: {template_id}")
                    continue
                
                if success:
                    created_count += 1
                    print(f"✅ Template recreado: {template_data['name']}")
                else:
                    print(f"❌ Error recreando template: {result_id}")
            
            print(f"✅ {created_count} templates cargados desde {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando templates: {e}")
            return False
    
    async def get_world_overview_with_mcp(self) -> Dict[str, Any]:
        """Obtiene vista general del mundo con contexto MCP"""
        stats = await self.mcp_provider.get_mcp_memory_stats()
        
        # Estadísticas adicionales del editor
        editor_stats = {
            "templates_in_cache": len(self.templates_cache),
            "presets_available": {
                "locations": len(self.location_presets),
                "objects": len(self.object_presets)
            }
        }
        
        return {
            "mcp_stats": stats,
            "editor_stats": editor_stats,
            "world_status": "MCP Enhanced",
            "creation_capabilities": [
                "Smart location creation with context",
                "Object placement with validation", 
                "Event triggers with MCP integration",
                "Template-based rapid creation",
                "JSON import/export"
            ]
        }
    
    def close(self):
        """Cierra conexiones"""
        if self.memory_system:
            self.memory_system.close()

# Funciones de utilidad para creación rápida
def quick_location(name: str, description: str, theme: str = "", **kwargs) -> LocationTemplate:
    """Crea rápidamente un template de ubicación"""
    return LocationTemplate(
        id="",  # Se asignará al crear
        name=name,
        description=description,
        theme=theme,
        **kwargs
    )

def quick_object(name: str, description: str, location_id: str, object_type: str = "", **kwargs) -> ObjectTemplate:
    """Crea rápidamente un template de objeto"""
    return ObjectTemplate(
        id="",  # Se asignará al crear
        name=name,
        description=description,
        location_id=location_id,
        **kwargs
    )

def quick_event(name: str, description: str, trigger_type: str, trigger_condition: str, 
               action_type: str, action_data: Dict[str, Any], **kwargs) -> EventTemplate:
    """Crea rápidamente un template de evento"""
    return EventTemplate(
        id="",  # Se asignará al crear
        name=name,
        description=description,
        trigger_type=trigger_type,
        trigger_condition=trigger_condition,
        action_type=action_type,
        action_data=action_data,
        **kwargs
    )

# Ejemplo de uso y demostración
async def demo_mcp_world_editor():
    """Demostración completa del editor MCP"""
    print("🌍 MCP WORLD EDITOR - DEMOSTRACIÓN")
    print("=" * 50)
    
    # Inicializar editor
    editor = MCPWorldEditor("mcp_demo_world.db")
    if not await editor.initialize():
        return
    
    # 1. Crear una ubicación temática
    forest_location = quick_location(
        name="Bosque de los Susurros",
        description="Un bosque encantado donde los árboles parecen hablar entre ellos. La luz se filtra a través de hojas doradas creando patrones mágicos en el suelo cubierto de musgo.",
        theme="forest",
        connections={"sur": "entrada_castillo"},
        atmosphere="mágico y misterioso"
    )
    
    success, forest_id = await editor.create_location_with_mcp(forest_location)
    if success:
        print(f"✅ Bosque creado: {forest_id}")
    
    # 2. Crear objetos temáticos en el bosque
    magic_mushroom = quick_object(
        name="Seta Luminosa",
        description="Una seta que brilla con luz azulada. Al tocarla, emite un suave zumbido musical.",
        location_id=forest_id,
        object_type="treasure"
    )
    magic_mushroom.properties = {"light_source": True, "magical": True, "sound": "musical_hum"}
    magic_mushroom.ai_context = "Objeto mágico que puede usarse para iluminar áreas oscuras"
    
    success, mushroom_id = await editor.create_object_with_mcp(magic_mushroom)
    if success:
        print(f"✅ Seta mágica creada: {mushroom_id}")
    
    # 3. Crear un evento de entrada al bosque
    entrance_event = quick_event(
        name="Bienvenida al Bosque",
        description="Evento que se activa al entrar al bosque por primera vez",
        trigger_type="location_enter",
        trigger_condition=forest_id,
        action_type="message",
        action_data={
            "message": "Los árboles susurran tu nombre al entrar. Sientes que has llegado a un lugar especial.",
            "mood": "mysterious",
            "one_time": True
        }
    )
    
    success, event_id = await editor.create_event_with_mcp(entrance_event)
    if success:
        print(f"✅ Evento de entrada creado: {event_id}")
    
    # 4. Mostrar resumen del mundo
    overview = await editor.get_world_overview_with_mcp()
    print(f"\n📊 Resumen del mundo:")
    print(f"   Ubicaciones: {overview['mcp_stats']['total_locations']}")
    print(f"   Objetos: {overview['mcp_stats']['total_objects']}")
    print(f"   Eventos totales: {overview['mcp_stats']['total_events']}")
    print(f"   Templates en cache: {overview['editor_stats']['templates_in_cache']}")
    
    # 5. Exportar todo
    export_file = await editor.export_templates_to_json()
    print(f"\n💾 Mundo exportado a: {export_file}")
    
    # 6. Demostrar contexto MCP
        if forest_id:
            print(f"\n🔍 Contexto MCP del bosque:")
            context = await editor.mcp_provider.generate_world_context_for_ai(
                forest_id, 
                query="seta luminosa"
            )
            print(context[:500] + "..." if len(context) > 500 else context)

    # =============================================================================
    # MÉTODOS WRAPPER PARA WEB API
    # =============================================================================
    
    async def create_location_with_mcp(self, name: str, description: str, preset: str = None, 
                                      connections: List[str] = None, properties: Dict = None) -> Dict[str, Any]:
        """Wrapper para crear ubicación desde parámetros directos (API web)"""
        try:
            # Crear template desde parámetros
            template = LocationTemplate(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                connections={conn: conn for conn in (connections or [])},
                properties=properties or {}
            )
            
            # Aplicar preset si se especifica
            if preset and preset in self.location_presets:
                preset_data = self.location_presets[preset]
                template.atmosphere = preset_data.get("atmosphere", "")
                template.lighting = preset_data.get("lighting", "normal")
                template.properties.update(preset_data.get("properties", {}))
            
            # Crear ubicación
            success, location_id = await self.create_location_with_mcp_template(template)
            
            return {
                "success": success,
                "location_id": location_id,
                "template": asdict(template)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_object_with_mcp(self, name: str, description: str, location_name: str, 
                                    preset: str = None, properties: Dict = None) -> Dict[str, Any]:
        """Wrapper para crear objeto desde parámetros directos (API web)"""
        try:
            # Crear template desde parámetros
            template = ObjectTemplate(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                location_name=location_name,
                properties=properties or {}
            )
            
            # Aplicar preset si se especifica
            if preset and preset in self.object_presets:
                preset_data = self.object_presets[preset]
                template.properties.update(preset_data.get("properties", {}))
                template.keywords = preset_data.get("keywords", [])
                template.is_takeable = preset_data.get("is_takeable", True)
                template.is_usable = preset_data.get("is_usable", False)
            
            # Crear objeto
            success, object_id = await self.create_object_with_mcp_template(template)
            
            return {
                "success": success,
                "object_id": object_id,
                "template": asdict(template)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_event_with_mcp(self, name: str, description: str, trigger_type: str,
                                   trigger_value: str, action_type: str, action_data: Dict = None,
                                   properties: Dict = None) -> Dict[str, Any]:
        """Wrapper para crear evento desde parámetros directos (API web)"""
        try:
            # Crear template desde parámetros
            template = EventTemplate(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                trigger_type=trigger_type,
                trigger_value=trigger_value,
                action_type=action_type,
                action_data=action_data or {},
                properties=properties or {}
            )
            
            # Crear evento
            success, event_id = await self.create_event_with_mcp_template(template)
            
            return {
                "success": success,
                "event_id": event_id,
                "template": asdict(template)
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
    
    # Renombrar métodos originales para evitar conflictos
    async def create_location_with_mcp_template(self, template: LocationTemplate, 
                                               ai_enhance: bool = True) -> Tuple[bool, str]:    editor.close()
    print("\n✅ Demostración completada")

if __name__ == "__main__":
    asyncio.run(demo_mcp_world_editor())
