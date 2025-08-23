
# Adventure Game con Sistema de Memoria Perfecta, MCP y Vector Search v1.1.0
import asyncio
import json
import aiohttp
import logging
from typing import Dict, Any, Optional, List
from memory_system import PerfectMemorySystem
from mcp_integration import MCPContextProvider
from enhanced_mcp import EnhancedMCPProvider
from vector_search import VectorSearchEngine

class OllamaClient:
    """Cliente real para conectar con Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = None
    
    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def generate(self, model: str, prompt: str, system: str = None) -> str:
        """Genera respuesta usando Ollama"""
        await self._ensure_session()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "Sin respuesta").strip()
                else:
                    return f"Error de Ollama: {response.status}"
        except Exception as e:
            return f"Error conectando con Ollama: {e}"
    
    async def close(self):
        if self.session:
            await self.session.close()
            print("🔒 Conexión con Ollama cerrada")

class IntelligentAdventureGame:
    """
    Juego de aventura inteligente con memoria perfecta y búsqueda vectorial
    
    Versión 1.1.0 - Nuevas características:
    - Sistema de búsqueda semántica con ChromaDB
    - Análisis de patrones de objetos y ubicaciones
    - Contexto MCP enriquecido con similitud vectorial
    - Recomendaciones inteligentes basadas en embeddings
    """
    
    def __init__(self, memory_db_path: str = "adventure_world.db", model: str = "llama3.2"):
        self.memory = PerfectMemorySystem(memory_db_path)
        
        # Sistema MCP mejorado con búsqueda vectorial
        self.mcp = EnhancedMCPProvider(self.memory, memory_db_path)
        
        self.model = model
        self.ollama = OllamaClient()
        self.current_location_id = None
        self.player_id = "player"
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        print(f"🎮 IntelligentAdventureGame v1.1.0 inicializado")
        print(f"   📊 Modelo: {model}")
        print(f"   💾 Base de datos: {memory_db_path}")
        print(f"   🧠 Memoria perfecta: ACTIVA")
        print(f"   🔍 Búsqueda vectorial: ACTIVANDO...")
    
    async def initialize_world(self):
        """Inicializa el mundo del juego si no existe"""
        
        # Verificar si ya existe el mundo
        cursor = self.memory.db_connection.execute("SELECT COUNT(*) FROM locations")
        location_count = cursor.fetchone()[0]
        
        if location_count == 0:
            print("🏗️ Creando mundo inicial...")
            
            # Crear ubicaciones iniciales
            entrance = await self.memory.create_location(
                "Entrada del Castillo",
                "Te encuentras en la entrada de un castillo abandonado. Grandes puertas de roble se alzan ante ti, cubiertas de musgo y oxidación.",
                connections={"norte": "hall_principal", "sur": "camino_bosque"},
                properties={"lighting": "dim", "atmosphere": "mysterious"}
            )
            
            hall = await self.memory.create_location(
                "Hall Principal", 
                "Un gran salón con techos abovedados. Antorchas apagadas cuelgan de las paredes de piedra.",
                connections={"sur": "entrada", "este": "biblioteca", "oeste": "cocina"},
                properties={"lighting": "dark", "echo": True}
            )
            
            library = await self.memory.create_location(
                "Biblioteca",
                "Estanterías enormes llenas de libros polvorientos se extienden hasta el techo.",
                connections={"oeste": "hall_principal"},
                properties={"knowledge": True, "lighting": "dim"}
            )
            
            kitchen = await self.memory.create_location(
                "Cocina",
                "Una cocina medieval con un gran horno de piedra. Utensilios oxidados cuelgan de ganchos.",
                connections={"este": "hall_principal"},
                properties={"cooking": True, "storage": True}
            )
            
            # Crear objetos iniciales
            await self.memory.create_object(
                "llave oxidada",
                "Una pequeña llave de hierro cubierta de óxido. Parece muy antigua.",
                entrance.id,
                properties={"material": "iron", "condition": "rusty", "opens": "mysterious_door"}
            )
            
            await self.memory.create_object(
                "libro de hechizos",
                "Un grimorio encuadernado en cuero negro con símbolos místicos.",
                library.id,
                properties={"type": "spellbook", "spells": ["light", "unlock"], "condition": "ancient"}
            )
            
            await self.memory.create_object(
                "martillo del herrero",
                "Un pesado martillo de forja con el mango desgastado por años de uso.",
                kitchen.id,
                properties={"material": "steel_wood", "weight": 2.5, "condition": "worn", "craft_tool": True}
            )
            
            # Establecer ubicación inicial
            self.current_location_id = entrance.id
            
            print("✅ Mundo creado exitosamente")
        else:
            # Mundo ya existe, obtener ubicación por defecto
            cursor = self.memory.db_connection.execute("SELECT id FROM locations LIMIT 1")
            self.current_location_id = cursor.fetchone()[0]
            print("🌍 Mundo existente cargado")
    
    async def process_command_async(self, command: str) -> str:
        """Procesa comando del jugador usando IA con contexto perfecto y búsqueda vectorial"""
        
        if not self.current_location_id:
            await self.initialize_world()
        
        # Inicializar búsqueda vectorial si no está lista
        await self.mcp.initialize_vector_search()
        
        # Registrar comando del jugador
        await self.memory._record_event(
            event_type="player_command",
            actor=self.player_id,
            action=f"issued command: {command}",
            target=None,
            location_id=self.current_location_id,
            context={"command": command, "raw_input": True}
        )
        
        # Detectar comandos de búsqueda vectorial especiales
        if await self._handle_vector_search_commands(command):
            return await self._process_vector_search_command(command)
        
        # Obtener contexto enriquecido para la IA
        player_inventory = await self._get_player_inventory()
        recent_actions = await self._get_recent_actions(limit=3)
        
        world_context = await self.mcp.generate_enhanced_world_context_for_ai(
            self.current_location_id,
            player_inventory,
            recent_actions
        )
        
        # Preparar prompt mejorado para la IA
        system_prompt = f"""
Eres el narrador de un juego de aventura con MEMORIA PERFECTA y BÚSQUEDA SEMÁNTICA AVANZADA.

NUEVAS CAPACIDADES v1.1.0:
- Puedes encontrar objetos por similitud semántica
- Análisis de patrones de objetos y ubicaciones
- Recomendaciones inteligentes basadas en contexto
- Búsqueda por función y características

COMANDOS ESPECIALES DISPONIBLES:
- "buscar objetos como X" - Encuentra objetos similares
- "buscar herramientas de Y" - Busca por función/categoría  
- "analizar patrones aquí" - Analiza patrones de ubicación
- "recomendar objetos" - Sugerencias inteligentes

REGLAS IMPORTANTES:
1. Usa SOLO la información del contexto del mundo proporcionado
2. Todos los objetos mencionados EXISTEN realmente en el juego
3. Las ubicaciones y sus conexiones son exactas
4. Responde en español de forma inmersiva y descriptiva
5. Si el jugador interactúa con objetos, actualiza sus estados si es apropiado
6. Mantén consistencia absoluta con la información del mundo
7. USA las nuevas capacidades de búsqueda para enriquecer las respuestas

CONTEXTO ACTUAL DEL MUNDO (ENRIQUECIDO):
{world_context}

Responde al comando del jugador de forma inmersiva. Si el comando implica cambios en el mundo, describe claramente lo que ocurre.
"""
        
        user_prompt = f"Comando del jugador: {command}"
        
        # Obtener respuesta de la IA
        response = await self.ollama.generate(
            model=self.model,
            prompt=user_prompt,
            system=system_prompt
        )
        
        # Procesar acciones implícitas en la respuesta
        await self._process_game_actions(command, response)
        
        return response
    
    async def _process_game_actions(self, command: str, ai_response: str):
        """Procesa acciones del juego basadas en comando y respuesta"""
        
        command_lower = command.lower()
        
        # Detectar movimiento
        movement_commands = {
            "norte": "norte", "north": "norte", "n": "norte",
            "sur": "sur", "south": "sur", "s": "sur", 
            "este": "este", "east": "este", "e": "este",
            "oeste": "oeste", "west": "oeste", "o": "oeste"
        }
        
        for cmd, direction in movement_commands.items():
            if cmd in command_lower:
                await self._attempt_movement(direction)
                break
        
        # Detectar tomar objetos
        if "tomar" in command_lower or "coger" in command_lower or "agarrar" in command_lower:
            await self._attempt_take_object(command)
        
        # Detectar dejar objetos  
        if "dejar" in command_lower or "soltar" in command_lower:
            await self._attempt_drop_object(command)
    
    async def _attempt_movement(self, direction: str):
        """Intenta mover al jugador en una dirección"""
        
        # Obtener conexiones de la ubicación actual
        cursor = self.memory.db_connection.execute("""
            SELECT connections FROM locations WHERE id = ?
        """, (self.current_location_id,))
        
        row = cursor.fetchone()
        if row:
            connections = json.loads(row[0] or "{}")
            if direction in connections:
                new_location_id = connections[direction]
                old_location_id = self.current_location_id
                self.current_location_id = new_location_id
                
                # Registrar movimiento
                await self.memory._record_event(
                    event_type="player_movement",
                    actor=self.player_id,
                    action=f"moved {direction} from {old_location_id} to {new_location_id}",
                    target=new_location_id,
                    location_id=new_location_id,
                    context={
                        "direction": direction,
                        "from_location": old_location_id,
                        "to_location": new_location_id
                    }
                )
    
    async def _attempt_take_object(self, command: str):
        """Intenta tomar un objeto mencionado en el comando"""
        
        # Buscar objetos en la ubicación actual
        objects = await self.memory.get_objects_in_location(self.current_location_id)
        
        command_lower = command.lower()
        for obj in objects:
            if obj.name.lower() in command_lower:
                # Mover objeto al inventario del jugador
                success = await self.memory.move_object(
                    obj.id, 
                    "inventory_player", 
                    actor=self.player_id
                )
                if success:
                    await self.memory._record_event(
                        event_type="object_taken",
                        actor=self.player_id,
                        action=f"took {obj.name}",
                        target=obj.id,
                        location_id=self.current_location_id,
                        context={"object_name": obj.name, "action": "take"}
                    )
                break
    
    async def _attempt_drop_object(self, command: str):
        """Intenta dejar un objeto del inventario"""
        
        # Buscar objetos en el inventario del jugador
        inventory_objects = await self.memory.get_objects_in_location("inventory_player")
        
        command_lower = command.lower()
        for obj in inventory_objects:
            if obj.name.lower() in command_lower:
                # Mover objeto a la ubicación actual
                success = await self.memory.move_object(
                    obj.id,
                    self.current_location_id,
                    actor=self.player_id
                )
                if success:
                    await self.memory._record_event(
                        event_type="object_dropped",
                        actor=self.player_id,
                        action=f"dropped {obj.name}",
                        target=obj.id,
                        location_id=self.current_location_id,
                        context={"object_name": obj.name, "action": "drop"}
                    )
                break
    
    async def get_inventory(self) -> str:
        """Obtiene inventario del jugador"""
        inventory_objects = await self.memory.get_objects_in_location("inventory_player")
        
        if not inventory_objects:
            return "Tu inventario está vacío."
        
        inventory_text = "🎒 Tu inventario contiene:\n"
        for obj in inventory_objects:
            inventory_text += f"- {obj.name}: {obj.description}\n"
            if obj.properties:
                props = [f"{k}: {v}" for k, v in obj.properties.items()]
                inventory_text += f"  ({', '.join(props)})\n"
        
        return inventory_text
    
    async def get_world_stats(self) -> str:
        """Obtiene estadísticas del mundo incluyendo búsqueda vectorial"""
        stats = await self.mcp.get_mcp_memory_stats()
        vector_stats = await self.mcp.get_vector_search_stats()
        
        vector_info = ""
        if vector_stats.get('status') == 'active':
            vector_info = f"""
🔍 BÚSQUEDA VECTORIAL:
- Estado: {vector_stats['status']}
- Objetos indexados: {vector_stats.get('objects', {}).get('document_count', 0)}
- Ubicaciones indexadas: {vector_stats.get('locations', {}).get('document_count', 0)}
- Eventos indexados: {vector_stats.get('events', {}).get('document_count', 0)}"""
        else:
            vector_info = f"🔍 BÚSQUEDA VECTORIAL: {vector_stats.get('status', 'no disponible')}"
        
        return f"""
🌍 ESTADÍSTICAS DEL MUNDO v1.1.0:
- Ubicaciones: {stats['total_locations']}
- Objetos: {stats['total_objects']}  
- Eventos registrados: {stats['total_events']}
- Integridad de memoria: {stats['memory_integrity']}
- Primer evento: {stats['first_recorded_event'] or 'N/A'}
- Último evento: {stats['last_recorded_event'] or 'N/A'}
{vector_info}
"""
    
    async def _handle_vector_search_commands(self, command: str) -> bool:
        """Detecta si el comando requiere búsqueda vectorial especial"""
        vector_keywords = [
            "buscar objetos", "buscar herramientas", "encontrar similar",
            "objetos como", "herramientas de", "analizar patrones",
            "recomendar objetos", "objetos parecidos", "similar a"
        ]
        
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in vector_keywords)
    
    async def _process_vector_search_command(self, command: str) -> str:
        """Procesa comandos específicos de búsqueda vectorial"""
        command_lower = command.lower()
        
        try:
            # Buscar objetos similares
            if "buscar objetos como" in command_lower or "objetos parecidos" in command_lower:
                # Extraer el objeto de referencia
                if "como" in command_lower:
                    search_term = command_lower.split("como")[1].strip()
                else:
                    search_term = command_lower.replace("objetos parecidos", "").strip()
                
                results = await self.mcp.search_objects_by_description(search_term, limit=5)
                return self._format_search_results("objetos similares", results, search_term)
            
            # Buscar herramientas por función
            elif "buscar herramientas de" in command_lower or "herramientas para" in command_lower:
                if "de" in command_lower:
                    search_term = command_lower.split("de")[1].strip()
                else:
                    search_term = command_lower.split("para")[1].strip()
                
                results = await self.mcp.find_objects_by_pattern(f"herramientas {search_term}")
                return self._format_search_results("herramientas especializadas", results, search_term)
            
            # Analizar patrones de ubicación
            elif "analizar patrones" in command_lower:
                if not await self.mcp.vector_initialized:
                    return "🔍 La búsqueda vectorial aún no está disponible."
                
                patterns = await self.mcp.vector_engine.analyze_location_patterns(self.current_location_id)
                return self._format_pattern_analysis(patterns)
            
            # Recomendaciones generales
            elif "recomendar objetos" in command_lower:
                player_inventory = await self._get_player_inventory()
                if not player_inventory:
                    results = await self.mcp.search_objects_by_description("herramientas útiles", limit=3)
                else:
                    # Buscar objetos complementarios al último en inventario
                    last_object = player_inventory[-1]
                    results = await self.mcp.vector_engine.find_similar_objects(last_object, limit=3)
                    
                return self._format_recommendations(results)
            
            else:
                # Búsqueda general
                results = await self.mcp.search_objects_by_description(command, limit=5)
                return self._format_search_results("búsqueda general", results, command)
                
        except Exception as e:
            self.logger.error(f"Error en búsqueda vectorial: {e}")
            return f"🔍 Error en búsqueda vectorial: {str(e)}"
    
    def _format_search_results(self, search_type: str, results: List[Dict], query: str) -> str:
        """Formatea resultados de búsqueda vectorial"""
        if not results:
            return f"🔍 No se encontraron {search_type} para '{query}'."
        
        response = f"🔍 **{search_type.upper()}** para '{query}':\n\n"
        
        for i, result in enumerate(results[:5], 1):
            name = result.get('name', 'Objeto sin nombre')
            location = result.get('location_id', 'Ubicación desconocida')
            score = result.get('similarity_score', 0)
            
            response += f"{i}. **{name}**\n"
            response += f"   📍 Ubicación: {location}\n"
            response += f"   🎯 Relevancia: {score:.1%}\n"
            
            properties = result.get('properties', {})
            if properties:
                prop_list = [f"{k}: {v}" for k, v in properties.items() if v]
                if prop_list:
                    response += f"   📊 Propiedades: {', '.join(prop_list[:3])}\n"
            
            response += "\n"
        
        return response
    
    def _format_pattern_analysis(self, patterns: Dict[str, Any]) -> str:
        """Formatea análisis de patrones"""
        if not patterns.get('patterns'):
            return "🔍 No se detectaron patrones significativos en esta ubicación."
        
        response = f"🔍 **ANÁLISIS DE PATRONES** - {self.current_location_id}:\n\n"
        response += f"📊 Objetos analizados: {patterns.get('total_objects', 0)}\n"
        response += f"📈 Patrones encontrados: {len(patterns['patterns'])}\n\n"
        
        for i, pattern in enumerate(patterns['patterns'][:5], 1):
            response += f"{i}. **{pattern['object1']}** ↔ **{pattern['object2']}**\n"
            response += f"   🎯 Similitud: {pattern['similarity']:.1%}\n"
            response += f"   📝 Tipo: {pattern.get('pattern_type', 'semantic_similarity')}\n\n"
        
        response += f"💡 **Resumen**: {patterns.get('summary', 'Análisis completado')}"
        
        return response
    
    def _format_recommendations(self, results: List) -> str:
        """Formatea recomendaciones de objetos"""
        if not results:
            return "🔍 No hay recomendaciones disponibles en este momento."
        
        response = "💡 **RECOMENDACIONES INTELIGENTES**:\n\n"
        
        for i, result in enumerate(results[:3], 1):
            if isinstance(result, dict):
                name = result.get('name', 'Objeto recomendado')
                score = result.get('similarity_score', 0)
                response += f"{i}. **{name}** (relevancia: {score:.1%})\n"
            else:
                # Es un SearchResult
                name = result.document.metadata.get('name', 'Objeto recomendado')
                score = result.similarity_score
                response += f"{i}. **{name}** (relevancia: {score:.1%})\n"
        
        response += "\n💬 Estas recomendaciones se basan en análisis semántico de tus objetos actuales."
        
        return response
    
    async def _get_player_inventory(self) -> List[str]:
        """Obtiene lista de IDs de objetos en el inventario del jugador"""
        try:
            inventory_objects = await self.memory.get_objects_in_location("inventory_player")
            return [obj.id for obj in inventory_objects]
        except:
            return []
    
    async def _get_recent_actions(self, limit: int = 5) -> List[str]:
        """Obtiene acciones recientes del jugador"""
        try:
            cursor = self.memory.db_connection.execute("""
                SELECT action FROM game_events 
                WHERE actor = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (self.player_id, limit))
            
            return [row[0] for row in cursor.fetchall()]
        except:
            return []
    
    async def close(self):
        """Cierra todas las conexiones"""
        await self.ollama.close()
        self.memory.close()
        print("🎮 Juego cerrado correctamente")

# Compatibilidad con el demo existente
class VectorMemoryProvider:
    """Wrapper de compatibilidad"""
    def __init__(self, db_name):
        print(f"⚠️ VectorMemoryProvider es legacy - usa PerfectMemorySystem")
        self.db_name = db_name
