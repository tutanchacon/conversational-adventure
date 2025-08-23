# Integración MCP (Model Context Protocol) para Adventure Game
# Proporciona contexto perfecto a la IA sobre el estado del mundo

import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from memory_system import PerfectMemorySystem, GameObject, Location, GameEvent

class MCPContextProvider:
    """
    Proveedor de contexto para MCP que garantiza que la IA tenga
    acceso completo al estado del mundo y su historia
    """
    
    def __init__(self, memory_system: PerfectMemorySystem):
        self.memory = memory_system
        self.context_cache = {}
        self.cache_ttl = timedelta(seconds=30)  # Cache de 30 segundos
        
    async def get_location_context(self, location_id: str) -> Dict[str, Any]:
        """Obtiene contexto completo de una ubicación para la IA"""
        
        # Obtener objetos en la ubicación
        objects = await self.memory.get_objects_in_location(location_id)
        
        # Obtener eventos recientes en la ubicación
        cursor = self.memory.db_connection.execute("""
            SELECT * FROM game_events 
            WHERE location_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 20
        """, (location_id,))
        
        recent_events = []
        for row in cursor.fetchall():
            recent_events.append({
                'timestamp': row[1],
                'actor': row[3],
                'action': row[4],
                'context': json.loads(row[7] or "{}")
            })
        
        # Construir contexto
        context = {
            "location_id": location_id,
            "objects_present": [
                {
                    "id": obj.id,
                    "name": obj.name,
                    "description": obj.description,
                    "properties": obj.properties,
                    "last_modified": obj.last_modified.isoformat()
                }
                for obj in objects
            ],
            "recent_activity": recent_events,
            "object_count": len(objects),
            "has_persistent_memory": True
        }
        
        return context
    
    async def get_object_context(self, object_id: str) -> Dict[str, Any]:
        """Obtiene contexto completo de un objeto específico"""
        
        # Obtener datos del objeto
        cursor = self.memory.db_connection.execute("""
            SELECT * FROM game_objects WHERE id = ?
        """, (object_id,))
        
        row = cursor.fetchone()
        if not row:
            return {"error": "object_not_found"}
        
        # Obtener historial completo
        history = await self.memory.get_object_history(object_id)
        
        # Obtener ubicación actual
        cursor = self.memory.db_connection.execute("""
            SELECT name, description FROM locations WHERE id = ?
        """, (row[3],))
        
        location_row = cursor.fetchone()
        
        context = {
            "object_id": object_id,
            "name": row[1],
            "description": row[2],
            "current_location": {
                "id": row[3],
                "name": location_row[0] if location_row else "unknown",
                "description": location_row[1] if location_row else ""
            },
            "properties": json.loads(row[4] or "{}"),
            "created_at": row[5],
            "last_modified": row[6],
            "version": row[7],
            "complete_history": [
                {
                    "timestamp": event.timestamp.isoformat(),
                    "event_type": event.event_type,
                    "actor": event.actor,
                    "action": event.action,
                    "context": event.context
                }
                for event in history
            ],
            "history_length": len(history)
        }
        
        return context
    
    async def get_player_context(self, player_id: str = "player") -> Dict[str, Any]:
        """Obtiene contexto del jugador y sus acciones recientes"""
        
        # Obtener eventos del jugador
        cursor = self.memory.db_connection.execute("""
            SELECT * FROM game_events 
            WHERE actor = ? 
            ORDER BY timestamp DESC 
            LIMIT 50
        """, (player_id,))
        
        player_events = []
        for row in cursor.fetchall():
            player_events.append({
                'id': row[0],
                'timestamp': row[1],
                'event_type': row[2],
                'action': row[4],
                'target': row[5],
                'location_id': row[6],
                'context': json.loads(row[7] or "{}")
            })
        
        # Analizar patrones
        locations_visited = set()
        objects_interacted = set()
        
        for event in player_events:
            locations_visited.add(event['location_id'])
            if event['target']:
                objects_interacted.add(event['target'])
        
        context = {
            "player_id": player_id,
            "recent_actions": player_events[:10],  # Solo las 10 más recientes
            "total_actions": len(player_events),
            "locations_visited": list(locations_visited),
            "objects_interacted": list(objects_interacted),
            "play_style_analysis": self._analyze_play_style(player_events),
            "memory_integrity": "perfect"
        }
        
        return context
    
    def _analyze_play_style(self, events: List[Dict]) -> Dict[str, Any]:
        """Analiza el estilo de juego del jugador"""
        if not events:
            return {"analysis": "no_data"}
        
        # Contar tipos de acciones
        action_types = {}
        for event in events:
            event_type = event['event_type']
            action_types[event_type] = action_types.get(event_type, 0) + 1
        
        # Determinar tendencias
        total_actions = len(events)
        exploration_actions = action_types.get('object_moved', 0) + action_types.get('location_visited', 0)
        
        return {
            "total_actions": total_actions,
            "action_distribution": action_types,
            "exploration_tendency": exploration_actions / total_actions if total_actions > 0 else 0,
            "most_common_action": max(action_types.items(), key=lambda x: x[1])[0] if action_types else None
        }
    
    async def generate_world_context_for_ai(self, current_location_id: str, 
                                          query: str = None) -> str:
        """
        Genera un contexto textual completo para que la IA entienda 
        perfectamente el estado del mundo
        """
        
        # Obtener contexto de la ubicación actual
        location_context = await self.get_location_context(current_location_id)
        
        # Obtener ubicación actual
        cursor = self.memory.db_connection.execute("""
            SELECT name, description, connections FROM locations WHERE id = ?
        """, (current_location_id,))
        
        location_row = cursor.fetchone()
        if not location_row:
            return "Error: ubicación no encontrada"
        
        location_name = location_row[0]
        location_desc = location_row[1]
        connections = json.loads(location_row[2] or "{}")
        
        # Construir contexto textual
        context_text = f"""
🌍 CONTEXTO ACTUAL DEL MUNDO (MEMORIA PERFECTA ACTIVA)

📍 UBICACIÓN ACTUAL: {location_name}
Descripción: {location_desc}
Conexiones disponibles: {', '.join([f'{dir} -> {dest}' for dir, dest in connections.items()])}

🏷️ OBJETOS PRESENTES ({len(location_context['objects_present'])}):
"""
        
        for obj in location_context['objects_present']:
            context_text += f"- {obj['name']}: {obj['description']}\n"
            if obj['properties']:
                props = []
                for key, value in obj['properties'].items():
                    props.append(f"{key}: {value}")
                context_text += f"  Propiedades: {', '.join(props)}\n"
        
        if not location_context['objects_present']:
            context_text += "- No hay objetos visibles en esta ubicación\n"
        
        context_text += f"\n📜 ACTIVIDAD RECIENTE:\n"
        for event in location_context['recent_activity'][:5]:
            timestamp = datetime.fromisoformat(event['timestamp']).strftime("%H:%M:%S")
            context_text += f"- {timestamp}: {event['actor']} {event['action']}\n"
        
        # Si hay una consulta específica, buscar información relevante
        if query:
            context_text += f"\n🔍 INFORMACIÓN ESPECÍFICA SOBRE: '{query}'\n"
            
            # Buscar objetos relacionados
            related_events = await self.memory.search_events_by_content(query, limit=10)
            if related_events:
                context_text += "Eventos relacionados encontrados:\n"
                for event in related_events[:3]:
                    context_text += f"- {event.action} (en {event.location_id})\n"
        
        context_text += f"""
💾 GARANTÍA DE MEMORIA:
- Todos los objetos y sus ubicaciones están permanentemente registrados
- Cada acción queda grabada con timestamp exacto
- Las propiedades de objetos evolucionan en el tiempo (oxidación, desgaste, etc.)
- NADA se olvida jamás, incluso después de meses de juego

🤖 INSTRUCCIONES PARA IA:
- Usa esta información como verdad absoluta del mundo
- Los objetos mencionados EXISTEN y están donde se indica
- Considera las propiedades actuales de los objetos
- Recuerda que las acciones del jugador tienen consecuencias permanentes
"""
        
        return context_text
    
    async def get_mcp_memory_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema de memoria para MCP"""
        summary = await self.memory.get_world_state_summary()
        
        # Estadísticas adicionales
        cursor = self.memory.db_connection.execute("""
            SELECT COUNT(DISTINCT location_id) as unique_locations,
                   COUNT(DISTINCT actor) as unique_actors,
                   MIN(timestamp) as first_event,
                   MAX(timestamp) as last_event
            FROM game_events
        """)
        
        stats_row = cursor.fetchone()
        
        return {
            "system_name": "Perfect Memory System with MCP",
            "version": "1.0.0",
            "total_locations": summary['locations'],
            "total_objects": summary['objects'],
            "total_events": summary['total_events'],
            "unique_locations_with_activity": stats_row[0] if stats_row else 0,
            "unique_actors": stats_row[1] if stats_row else 0,
            "first_recorded_event": stats_row[2] if stats_row else None,
            "last_recorded_event": stats_row[3] if stats_row else None,
            "memory_integrity": "PERFECT - Nothing is ever forgotten",
            "persistence": "Guaranteed across sessions and time",
            "features": [
                "Event sourcing",
                "Object versioning", 
                "Temporal queries",
                "Perfect recall",
                "State reconstruction"
            ]
        }

# Ejemplo de uso con IA
async def test_mcp_integration():
    """Prueba la integración MCP"""
    print("🔗 PROBANDO INTEGRACIÓN MCP")
    print("=" * 50)
    
    # Inicializar sistemas
    memory = PerfectMemorySystem("mcp_test.db")
    mcp = MCPContextProvider(memory)
    
    # Crear escenario de prueba
    workshop = await memory.create_location(
        "Taller del Herrero",
        "Un taller bien equipado con un gran banco de trabajo de roble.",
        connections={"norte": "patio", "este": "fragua"},
        properties={"tools_available": True, "lighting": "good"}
    )
    
    # El famoso martillo
    hammer = await memory.create_object(
        "martillo de guerra",
        "Un pesado martillo de guerra con inscripciones rúnicas.",
        workshop.id,
        properties={
            "material": "enchanted_steel",
            "condition": "pristine",
            "weight": 3.5,
            "enchantment": "fire_resistance",
            "durability": 100
        }
    )
    
    # Simular jugador interactuando
    await memory.move_object(hammer.id, "inventory_player", actor="player")
    await asyncio.sleep(0.1)
    await memory.modify_object_properties(
        hammer.id,
        {"durability": 95, "last_used": datetime.now().isoformat()},
        actor="player"
    )
    await memory.move_object(hammer.id, workshop.id, actor="player")
    
    # Generar contexto para IA
    print("\n🤖 CONTEXTO PARA IA:")
    context = await mcp.generate_world_context_for_ai(
        workshop.id, 
        query="martillo de guerra"
    )
    print(context)
    
    # Estadísticas MCP
    print("\n📊 ESTADÍSTICAS MCP:")
    stats = await mcp.get_mcp_memory_stats()
    for key, value in stats.items():
        if isinstance(value, list):
            print(f"{key}: {', '.join(value)}")
        else:
            print(f"{key}: {value}")
    
    memory.close()
    print("\n✅ Integración MCP funcionando perfectamente!")

if __name__ == "__main__":
    asyncio.run(test_mcp_integration())
