#!/usr/bin/env python3
"""
🎮 AI INTEGRATION - Adventure Game v3.0
Integra el sistema de IA avanzado con el juego existente
"""

import asyncio
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import asdict

# Imports del sistema existente
# from adventure_game import AdventureGame  # No existe actualmente
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
        self.original_game = None
        self.memory_system = None
        self.ai_engine = None
        
        # Configuración de IA
        self.ai_config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "personality": AIPersonality.FRIENDLY,
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
            
            # 2. Inicializar juego original (comentado hasta tener la clase)
            # self.original_game = AdventureGame(self.db_path)
            
            # 3. Verificar API key de OpenAI
            if not self.ai_config["openai_api_key"]:
                logger.warning("⚠️ OPENAI_API_KEY not found. AI features will be limited.")
                self.ai_config["openai_api_key"] = "demo-key"
            
            # 4. Inicializar motor de IA
            self.ai_engine = await initialize_ai_engine(
                self.memory_system, 
                self.ai_config["openai_api_key"]
            )
            
            # 5. Configurar personalidad
            self.ai_engine.narrator.personality = self.ai_config["personality"]
            
            logger.info("✅ AI Adventure Game ready!")
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
            # Buscar en eventos recientes
            events = await self.memory_system.get_events_by_actor(player_id, limit=10)
            
            for event in events:
                if event.get('location_id'):
                    return event['location_id']
            
            # Default location
            return "starting_area"
            
        except Exception as e:
            logger.error(f"❌ Error getting player location: {e}")
            return "unknown_location"
    
    async def _process_original_command(self, player_id: str, command: str) -> Dict[str, Any]:
        """Procesar comando con la lógica original del juego"""
        try:
            # Simulación de procesamiento del juego original
            # Aquí se integraría con adventure_game.py
            
            command_lower = command.lower().strip()
            
            # Comandos básicos
            if "look" in command_lower or "mirar" in command_lower:
                return {
                    "action": "look",
                    "success": True,
                    "mechanical_result": "You observe your surroundings.",
                    "state_changes": []
                }
            elif "go" in command_lower or "move" in command_lower:
                return {
                    "action": "move",
                    "success": True,
                    "mechanical_result": "You attempt to move.",
                    "state_changes": ["location_change"]
                }
            elif "take" in command_lower or "get" in command_lower:
                return {
                    "action": "take",
                    "success": True,
                    "mechanical_result": "You attempt to take an item.",
                    "state_changes": ["inventory_change"]
                }
            else:
                return {
                    "action": "unknown",
                    "success": False,
                    "mechanical_result": "Command not recognized by game mechanics.",
                    "state_changes": []
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
        
        # Determinar si el comando fue exitoso
        success = original_result.get("success", False) or ai_response.confidence > 0.5
        
        # Combinar mensajes
        if original_result.get("success"):
            # Si el juego original procesó exitosamente, usar narrativa de IA
            message = ai_response.content
        else:
            # Si no, la IA puede intentar interpretar y responder creativamente
            message = ai_response.content
        
        # Resultado combinado
        result = {
            "success": success,
            "message": message,
            "suggestions": ai_response.suggestions,
            "ai_confidence": ai_response.confidence,
            "processing_time": ai_response.processing_time,
            
            # Datos del juego original
            "game_action": original_result.get("action", "unknown"),
            "mechanical_result": original_result.get("mechanical_result", ""),
            "state_changes": original_result.get("state_changes", []),
            
            # Datos de IA
            "ai_personality": ai_response.personality_applied.value,
            "context_used": ai_response.context_used,
            "generated_content": ai_response.generated_content,
            
            # Metadatos
            "timestamp": datetime.now().isoformat(),
            "player_id": player_id,
            "original_command": command
        }
        
        # Registrar evento en memoria
        await self._log_interaction(player_id, command, result)
        
        return result
    
    async def _log_interaction(self, player_id: str, command: str, result: Dict[str, Any]):
        """Registrar interacción en el sistema de memoria"""
        try:
            event = GameEvent(
                event_type="ai_interaction",
                timestamp=datetime.now(),
                actor_id=player_id,
                action_type="command",
                location_id=await self._get_player_location(player_id),
                details={
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
