#!/usr/bin/env python3
"""
🎮 AI INTEGRATION - Adventure Game v3.0
Integra el sistema de IA avanzado con el juego existente
"""

import asyncio
import os
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import asdict

# Imports del sistema existente
from adventure_game import IntelligentAdventureGame  # Usar el juego REAL
from memory_system import PerfectMemorySystem, GameEvent
from ai_engine import AIEngine, initialize_ai_engine, AIPersonality

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAdventureGame:
    """
    Adventure Game mejorado con IA avanzada
    Combina el juego original con el nuevo motor de IA
    """
    
    def __init__(self, db_path: str = "ai_adventure_game.db"):
        self.db_path = db_path
        self.original_game = None  # Será IntelligentAdventureGame
        self.memory_system = None
        self.ai_engine = None
        
        # Configuración de IA con Ollama
        from ai_engine import AILanguage
        
        # Mapear código de idioma a enum
        default_lang_code = os.getenv("AI_DEFAULT_LANGUAGE", "es")
        default_language = AILanguage.SPANISH  # fallback
        for lang in AILanguage:
            if lang.value == default_lang_code:
                default_language = lang
                break
        
        self.ai_config = {
            "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            "ollama_model": os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
            "personality": AIPersonality.FRIENDLY,
            "default_language": default_language,
            "enable_voice": False,
            "enable_predictions": True,
            "enable_content_generation": True
        }
        
        # Estadísticas
        self.stats = {
            "total_ai_responses": 0,
            "avg_response_time": 0.0,
            "player_satisfaction": 0.0,
            "ai_generated_content": 0
        }
        
        logger.info("🧠 AI Adventure Game initialized")
    
    async def initialize(self) -> bool:
        """Inicializar todos los sistemas"""
        try:
            logger.info("🚀 Initializing AI Adventure Game...")
            
            # 1. Inicializar memoria
            self.memory_system = PerfectMemorySystem(self.db_path)
            await self.memory_system.initialize()
            
            # 2. Inicializar juego original - USAR EL JUEGO REAL
            self.original_game = IntelligentAdventureGame(self.db_path)
            await self.original_game.initialize_world()
            logger.info("🎮 IntelligentAdventureGame inicializado")
            
            # 3. Configurar Ollama
            ollama_host = self.ai_config.get("ollama_host", "http://localhost:11434")
            logger.info(f"🤖 Using Ollama at: {ollama_host}")
            
            # 4. Inicializar motor de IA con Ollama
            self.ai_engine = await initialize_ai_engine(
                self.memory_system, 
                ollama_host
            )
            
            # 5. Configurar personalidad e idioma por defecto
            self.ai_engine.narrator.personality = self.ai_config["personality"]
            self.ai_engine.set_language(self.ai_config["default_language"])
            
            logger.info(f"✅ AI Adventure Game ready! Language: {self.ai_config['default_language'].value}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AI Adventure Game: {e}")
            return False
    
    async def process_command(self, player_id: str, command: str) -> Dict[str, Any]:
        """
        Procesar comando con IA mejorada
        Combina la lógica del juego original con respuestas de IA
        """
        start_time = datetime.now()
        
        try:
            # 1. Obtener ubicación actual del jugador
            current_location = await self._get_player_location(player_id)
            
            # 2. Procesar con juego original (para mecánicas)
            original_result = await self._process_original_command(player_id, command)
            
            # 3. Procesar con IA (para narrativa)
            ai_response = await self.ai_engine.process_player_input(
                player_id, command, current_location
            )
            
            # 4. Combinar resultados
            combined_result = await self._combine_results(
                original_result, ai_response, player_id, command
            )
            
            # 5. Actualizar estadísticas
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(processing_time, ai_response.confidence)
            
            logger.info(f"🎮 Command processed: '{command}' in {processing_time:.2f}s")
            return combined_result
            
        except Exception as e:
            logger.error(f"❌ Error processing command: {e}")
            return {
                "success": False,
                "message": "Sorry, I encountered an error processing your request.",
                "error": str(e),
                "suggestions": ["try again", "use simpler command", "type 'help'"]
            }
    
    async def _get_player_location(self, player_id: str) -> str:
        """Obtener ubicación actual del jugador"""
        try:
            # 1. Verificar si el juego original tiene la ubicación actual del jugador
            if self.original_game and hasattr(self.original_game, 'current_location_id'):
                if self.original_game.current_location_id:
                    return self.original_game.current_location_id
            
            # 2. Buscar en eventos recientes
            events = await self.memory_system.get_events_by_actor(player_id, limit=10)
            
            for event in events:
                if hasattr(event, 'location_id') and event.location_id:
                    return event.location_id
            
            # 3. Buscar la "Entrada del Castillo" como ubicación inicial
            try:
                locations = await self.original_game.memory.get_all_locations()
                for location in locations:
                    if "entrada" in location.name.lower() or "castle" in location.name.lower():
                        # Establecer como ubicación actual del jugador
                        if self.original_game:
                            self.original_game.current_location_id = location.id
                        logger.info(f"🎮 Player positioned at: {location.name} ({location.id})")
                        return location.id
                
                # Si no hay "entrada", usar la primera ubicación disponible
                if locations:
                    first_location = locations[0]
                    if self.original_game:
                        self.original_game.current_location_id = first_location.id
                    logger.info(f"🎮 Player positioned at first location: {first_location.name}")
                    return first_location.id
            except Exception as e:
                logger.error(f"❌ Error finding initial location: {e}")
            
            # 4. Fallback: devolver None para que se maneje apropiadamente
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting player location: {e}")
            return None
    
    async def _process_original_command(self, player_id: str, command: str) -> Dict[str, Any]:
        """Procesar comando con la lógica original del juego"""
        try:
            if not self.original_game:
                return {
                    "action": "error",
                    "success": False,
                    "mechanical_result": "Game not initialized.",
                    "state_changes": []
                }
            
            command_lower = command.lower().strip()
            
            # Usar el juego REAL para comandos específicos
            if any(word in command_lower for word in ["inventory", "inventario", "mochila", "items"]):
                # Comando de inventario - usar método real del juego
                inventory_result = await self.original_game.get_inventory()
                return {
                    "action": "inventory",
                    "success": True,
                    "mechanical_result": inventory_result,
                    "state_changes": [],
                    "is_game_mechanic": True
                }
                
            elif any(word in command_lower for word in ["look", "mirar", "observar", "ver", "l", "examinar"]):
                # Comando mirar - delegar al juego original
                logger.info(f"🎮 Look command detected: '{command}'")
                return {
                    "action": "look", 
                    "success": True,
                    "mechanical_result": "Looking around...",
                    "state_changes": [],
                    "delegate_to_original": True
                }
                
            elif any(word in command_lower for word in ["take", "get", "tomar", "coger", "agarrar"]):
                # Comando tomar - delegar al juego original  
                return {
                    "action": "take",
                    "success": True,
                    "mechanical_result": "Attempting to take item...",
                    "state_changes": ["inventory_change"],
                    "delegate_to_original": True
                }
                
            elif any(word in command_lower for word in ["go", "move", "ir", "caminar", "north", "south", "east", "west", "norte", "sur", "este", "oeste", "n", "s", "e", "o"]):
                # Comando movimiento - delegar al juego original
                logger.info(f"🎮 Movement command detected: '{command}'")
                return {
                    "action": "move",
                    "success": True,
                    "mechanical_result": "Attempting to move...",
                    "state_changes": ["location_change"],
                    "delegate_to_original": True
                }
                
            elif any(word in command_lower for word in ["drop", "dejar", "soltar"]):
                # Comando dejar - delegar al juego original
                return {
                    "action": "drop",
                    "success": True,
                    "mechanical_result": "Attempting to drop item...",
                    "state_changes": ["inventory_change"],
                    "delegate_to_original": True
                }
                
            else:
                # Comando no reconocido - usar IA para respuesta natural
                return {
                    "action": "ai_response",
                    "success": True,
                    "mechanical_result": "Processing with AI...",
                    "state_changes": [],
                    "use_ai_only": True
                }
                
        except Exception as e:
            logger.error(f"❌ Error in original command processing: {e}")
            return {
                "action": "error",
                "success": False,
                "mechanical_result": "Error in game mechanics.",
                "state_changes": []
            }
    
    async def _combine_results(self, original_result: Dict, ai_response, 
                             player_id: str, command: str) -> Dict[str, Any]:
        """Combinar resultados del juego original con respuesta de IA"""
        
        # CASO 1: Comando de inventario - usar resultado directo del juego
        if original_result.get("action") == "inventory":
            return {
                "success": True,
                "message": original_result.get("mechanical_result"),
                "suggestions": ["look around", "examine items", "use item"],
                "ai_confidence": 1.0,
                "processing_time": 0.1,
                "game_action": "inventory",
                "mechanical_result": original_result.get("mechanical_result"),
                "state_changes": [],
                "ai_personality": ai_response.personality_applied.value,
                "context_used": "game_mechanics",
                "generated_content": {},
                "timestamp": datetime.now().isoformat(),
                "player_id": player_id,
                "original_command": command
            }
        
        # CASO 2: Comandos delegados al juego original
        if original_result.get("delegate_to_original"):
            # Llamar al juego original para obtener el resultado real
            original_response = await self._call_original_game(command, player_id)
            
            # Combinar con narrativa de IA si es necesario
            return {
                "success": True,
                "message": original_response,
                "suggestions": ai_response.suggestions,
                "ai_confidence": ai_response.confidence,
                "processing_time": ai_response.processing_time,
                "game_action": original_result.get("action"),
                "mechanical_result": original_response,
                "state_changes": original_result.get("state_changes", []),
                "ai_personality": ai_response.personality_applied.value,
                "context_used": ai_response.context_used,
                "generated_content": ai_response.generated_content,
                "timestamp": datetime.now().isoformat(),
                "player_id": player_id,
                "original_command": command
            }
        
        # CASO 3: Usar solo IA (conversación general)
        if original_result.get("use_ai_only"):
            return {
                "success": True,
                "message": ai_response.content,
                "suggestions": ai_response.suggestions,
                "ai_confidence": ai_response.confidence,
                "processing_time": ai_response.processing_time,
                "game_action": "ai_conversation",
                "mechanical_result": "AI conversation",
                "state_changes": [],
                "ai_personality": ai_response.personality_applied.value,
                "context_used": ai_response.context_used,
                "generated_content": ai_response.generated_content,
                "timestamp": datetime.now().isoformat(),
                "player_id": player_id,
                "original_command": command
            }
        
        # CASO 4: Combinar tradicional (respaldo)
        success = original_result.get("success", False) or ai_response.confidence > 0.5
        
        return {
            "success": success,
            "message": ai_response.content,
            "suggestions": ai_response.suggestions,
            "ai_confidence": ai_response.confidence,
            "processing_time": ai_response.processing_time,
            "game_action": original_result.get("action", "unknown"),
            "mechanical_result": original_result.get("mechanical_result", ""),
            "state_changes": original_result.get("state_changes", []),
            "ai_personality": ai_response.personality_applied.value,
            "context_used": ai_response.context_used,
            "generated_content": ai_response.generated_content,
            "timestamp": datetime.now().isoformat(),
            "player_id": player_id,
            "original_command": command
        }
        
        # Registrar evento en memoria
        await self._log_interaction(player_id, command, result)
        
        return result
    
    async def _call_original_game(self, command: str, player_id: str) -> str:
        """Llamar al juego original para procesar comando"""
        try:
            if not self.original_game:
                return "Game not initialized"
            
            # ✅ SOLUCIÓN: Usar el método correcto del juego original
            # El IntelligentAdventureGame tiene process_command_async que es lo que necesitamos
            logger.info(f"🎮 Calling original game with command: '{command}'")
            
            # Usar el procesador de comandos real del juego
            game_response = await self.original_game.process_command_async(command)
            
            logger.info(f"✅ Original game response received: {len(game_response)} chars")
            return game_response
                
        except Exception as e:
            logger.error(f"❌ Error calling original game: {e}")
            return f"Error processing command with original game: {e}"
    
    async def _get_location_description(self, location_id: str) -> str:
        """Obtener descripción de una ubicación"""
        try:
            # Si no hay location_id, crear una descripción inicial
            if not location_id:
                return "🌟 **¡Bienvenido al Adventure Game AI!**\n\nTe encuentras en el punto de entrada de una gran aventura.\nEl mundo se está cargando a tu alrededor...\n\n_Usa 'inventario' para ver tus objetos o continúa explorando._"
            
            # Método más eficiente: obtener ubicación específica
            location = await self.original_game.memory.get_location(location_id)
            
            if location:
                # Obtener objetos en la ubicación
                objects = await self.original_game.memory.get_objects_in_location(location_id)
                
                description = f"📍 **{location.name}**\n{location.description}\n"
                
                if objects:
                    description += "\n🎒 **Objetos visibles:**\n"
                    for obj in objects:
                        description += f"- **{obj.name}**: {obj.description}\n"
                else:
                    description += "\n_No hay objetos visibles aquí._"
                
                # Agregar información de conexiones si están disponibles
                if location.connections:
                    description += "\n🚪 **Salidas disponibles:**\n"
                    for direction, destination in location.connections.items():
                        description += f"- **{direction}** hacia {destination}\n"
                
                return description
            else:
                # Si no existe la ubicación específica, crear descripción básica
                return f"📍 **Ubicación Desconocida**\nTe encuentras en: {location_id}\nEsta es una ubicación misteriosa que aún no ha sido completamente explorada.\n\n_Usa 'inventario' para ver tus objetos o explora el área._"
                
        except Exception as e:
            logger.error(f"❌ Error getting location description: {e}")
            return f"📍 **Área Inexplorada**\nTe encuentras en un lugar misterioso.\nLa niebla envuelve el paisaje, haciendo difícil discernir los detalles.\n\n_Error: {str(e)}_"
    
    async def _handle_take_command(self, command: str) -> str:
        """Manejar comando de tomar objeto"""
        try:
            # Buscar objeto mencionado en el comando
            words = command.lower().split()
            object_words = [w for w in words if w not in ["take", "get", "tomar", "coger", "agarrar", "the", "el", "la"]]
            
            if not object_words:
                return "¿Qué quieres tomar?"
            
            # Buscar objeto en ubicación actual
            current_location = self.original_game.current_location_id or "starting_area"
            objects = await self.original_game.memory.get_objects_in_location(current_location)
            
            for obj in objects:
                if any(word in obj.name.lower() for word in object_words):
                    # Mover objeto al inventario
                    await self.original_game.memory.move_object_to_location(obj.id, "inventory_player")
                    return f"Has tomado: {obj.name}"
            
            return "No veo ese objeto aquí."
            
        except Exception as e:
            logger.error(f"❌ Error handling take command: {e}")
            return "Error tomando objeto"
    
    async def _handle_drop_command(self, command: str) -> str:
        """Manejar comando de dejar objeto"""
        try:
            # Buscar objeto mencionado en el comando
            words = command.lower().split()
            object_words = [w for w in words if w not in ["drop", "dejar", "soltar", "the", "el", "la"]]
            
            if not object_words:
                return "¿Qué quieres dejar?"
            
            # Buscar objeto en inventario
            inventory_objects = await self.original_game.memory.get_objects_in_location("inventory_player")
            
            for obj in inventory_objects:
                if any(word in obj.name.lower() for word in object_words):
                    # Mover objeto a ubicación actual
                    current_location = self.original_game.current_location_id or "starting_area"
                    await self.original_game.memory.move_object_to_location(obj.id, current_location)
                    return f"Has dejado: {obj.name}"
            
            return "No tienes ese objeto."
            
        except Exception as e:
            logger.error(f"❌ Error handling drop command: {e}")
            return "Error dejando objeto"
    
    async def _log_interaction(self, player_id: str, command: str, result: Dict[str, Any]):
        """Registrar interacción en el sistema de memoria"""
        try:
            event = GameEvent(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                event_type="ai_interaction",
                actor=player_id,
                action=f"executed command: {command}",
                target=None,
                location_id=await self._get_player_location(player_id),
                context={
                    "command": command,
                    "success": result["success"],
                    "ai_confidence": result["ai_confidence"],
                    "ai_personality": result["ai_personality"],
                    "processing_time": result["processing_time"]
                }
            )
            
            await self.memory_system.add_event(event)
            
        except Exception as e:
            logger.error(f"❌ Error logging interaction: {e}")
    
    def _update_stats(self, processing_time: float, confidence: float):
        """Actualizar estadísticas del sistema"""
        self.stats["total_ai_responses"] += 1
        
        # Actualizar tiempo promedio
        total_time = (self.stats["avg_response_time"] * 
                     (self.stats["total_ai_responses"] - 1) + processing_time)
        self.stats["avg_response_time"] = total_time / self.stats["total_ai_responses"]
        
        # Actualizar satisfacción (basada en confianza)
        total_satisfaction = (self.stats["player_satisfaction"] * 
                            (self.stats["total_ai_responses"] - 1) + confidence)
        self.stats["player_satisfaction"] = total_satisfaction / self.stats["total_ai_responses"]
    
    async def change_ai_personality(self, personality: AIPersonality) -> bool:
        """Cambiar personalidad del narrador de IA"""
        try:
            self.ai_engine.narrator.personality = personality
            self.ai_config["personality"] = personality
            
            logger.info(f"🎭 AI personality changed to: {personality.value}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error changing AI personality: {e}")
            return False
    
    async def get_ai_insights(self, player_id: str) -> Dict[str, Any]:
        """Obtener insights de IA sobre el jugador"""
        try:
            # Análisis de comportamiento
            behavior_analysis = await self.ai_engine.predictor.analyze_player_behavior(player_id)
            
            # Estadísticas del motor de IA
            ai_stats = await self.ai_engine.get_ai_stats()
            
            # Memorias más relevantes
            recent_memories = await self.ai_engine.rag_system.semantic_search(
                f"player {player_id}", limit=5
            )
            
            return {
                "player_behavior": behavior_analysis,
                "ai_engine_stats": ai_stats,
                "system_stats": self.stats,
                "recent_memories": recent_memories,
                "current_personality": self.ai_config["personality"].value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting AI insights: {e}")
            return {"error": str(e)}
    
    async def generate_world_content(self, content_type: str, 
                                   context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generar contenido del mundo usando IA"""
        try:
            if content_type == "location":
                return await self._generate_location(context)
            elif content_type == "npc":
                return await self._generate_npc(context)
            elif content_type == "object":
                return await self._generate_object(context)
            elif content_type == "quest":
                return await self._generate_quest(context)
            else:
                logger.warning(f"⚠️ Unknown content type: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error generating world content: {e}")
            return None
    
    async def _generate_location(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generar nueva ubicación con IA"""
        # Implementar generación de ubicaciones
        return {
            "id": f"ai_location_{datetime.now().timestamp()}",
            "name": "AI Generated Location",
            "description": "A mysterious place created by artificial intelligence.",
            "objects": [],
            "exits": {},
            "generated_by": "ai"
        }
    
    async def _generate_npc(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generar NPC con personalidad IA"""
        return {
            "id": f"ai_npc_{datetime.now().timestamp()}",
            "name": "AI Character",
            "personality": "friendly",
            "dialogue": ["Hello, traveler!"],
            "generated_by": "ai"
        }
    
    async def _generate_object(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generar objeto con IA"""
        return {
            "id": f"ai_object_{datetime.now().timestamp()}",
            "name": "Mysterious Item",
            "description": "An item created by artificial intelligence.",
            "properties": {},
            "generated_by": "ai"
        }
    
    async def _generate_quest(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generar quest con IA"""
        return {
            "id": f"ai_quest_{datetime.now().timestamp()}",
            "title": "AI Generated Quest",
            "description": "A quest designed by artificial intelligence.",
            "objectives": [],
            "rewards": [],
            "generated_by": "ai"
        }
    
    async def close(self):
        """Cerrar todos los sistemas"""
        try:
            if self.original_game:
                await self.original_game.close()
                
            if self.memory_system:
                await self.memory_system.close()
            
            logger.info("🛑 AI Adventure Game closed")
            
        except Exception as e:
            logger.error(f"❌ Error closing AI Adventure Game: {e}")

# Función de utilidad para crear instancia rápida
async def create_ai_game(db_path: str = "ai_adventure_game.db") -> AIAdventureGame:
    """Crear y inicializar instancia de AI Adventure Game"""
    game = AIAdventureGame(db_path)
    success = await game.initialize()
    
    if not success:
        raise Exception("Failed to initialize AI Adventure Game")
    
    return game

# Demo y testing
async def demo_ai_game():
    """Demostración del AI Adventure Game"""
    print("🧠 AI Adventure Game v3.0 Demo")
    print("=" * 40)
    
    try:
        # Crear juego
        game = await create_ai_game("demo_ai_game.db")
        
        # Comandos de prueba
        test_commands = [
            "look around",
            "go north to the mysterious forest",
            "examine the strange glowing stone",
            "create a magical sword",
            "talk to the wise old wizard"
        ]
        
        player_id = "demo_player"
        
        for command in test_commands:
            print(f"\n> {command}")
            result = await game.process_command(player_id, command)
            
            print(f"🎮 {result['message']}")
            if result.get('suggestions'):
                print(f"💡 Suggestions: {', '.join(result['suggestions'])}")
            print(f"⚡ AI Confidence: {result.get('ai_confidence', 0):.2f}")
            print(f"🎭 Personality: {result.get('ai_personality', 'unknown')}")
        
        # Mostrar insights
        print(f"\n📊 AI Insights:")
        insights = await game.get_ai_insights(player_id)
        print(f"  Play style: {insights['player_behavior'].get('play_style', 'unknown')}")
        print(f"  Total AI responses: {insights['system_stats']['total_ai_responses']}")
        print(f"  Avg response time: {insights['system_stats']['avg_response_time']:.2f}s")
        
        # Cerrar
        await game.close()
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")

if __name__ == "__main__":
    # Ejecutar demo
    asyncio.run(demo_ai_game())
