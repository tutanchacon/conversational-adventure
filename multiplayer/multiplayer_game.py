# 🎮 MULTIPLAYER GAME MANAGER - ORQUESTADOR PRINCIPAL

"""
Gestor Principal del Juego Multi-jugador
=======================================

Orquesta el juego multi-jugador, integrando el sistema de memoria perfecta
con la gestión de sesiones y sincronización del mundo.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

from .session_manager import MultiPlayerSessionManager, PlayerRole
from .world_synchronizer import WorldSynchronizer
from memory_system import PerfectMemorySystem

logger = logging.getLogger(__name__)

class MultiPlayerGameManager:
    """
    Gestor Principal del Juego Multi-jugador
    
    Integra todos los componentes del sistema multi-jugador:
    - Gestión de sesiones de jugadores
    - Sincronización del estado del mundo
    - Sistema de memoria perfecta
    - Comunicación en tiempo real
    """
    
    def __init__(self, memory_db_path: str = "multiplayer_world.db", max_players: int = 10):
        self.memory_system = PerfectMemorySystem(memory_db_path)
        self.session_manager = MultiPlayerSessionManager(max_players)
        self.world_synchronizer = WorldSynchronizer(self.memory_system, self.session_manager)
        
        self.game_state = {
            "server_started": datetime.now(),
            "world_initialized": False,
            "active_events": [],
            "server_stats": {}
        }
        
        logger.info(f"🎮 MultiPlayerGameManager inicializado")
        logger.info(f"   📊 Base de datos: {memory_db_path}")
        logger.info(f"   👥 Máximo jugadores: {max_players}")
    
    async def initialize_world(self):
        """Inicializa el mundo multi-jugador si no existe"""
        try:
            # Verificar si el mundo ya está inicializado
            locations = await self.memory_system.get_all_locations()
            
            if not locations:
                logger.info("🏗️ Creando mundo inicial multi-jugador...")
                await self._create_default_world()
                logger.info("✅ Mundo inicial creado")
            else:
                logger.info(f"🌍 Mundo existente cargado ({len(locations)} ubicaciones)")
            
            self.game_state["world_initialized"] = True
            
        except Exception as e:
            logger.error(f"❌ Error inicializando mundo: {e}")
            raise
    
    async def _create_default_world(self):
        """Crea el mundo inicial por defecto"""
        
        # Crear ubicaciones principales (sin conexiones inicialmente)
        entrance = await self.memory_system.create_location(
            "Entrada del Castillo Multiplayer",
            "Una gran entrada de piedra donde los aventureros se reúnen. "
            "Puedes ver otros jugadores explorando aquí."
        )
        
        hall = await self.memory_system.create_location(
            "Hall Principal",
            "Un amplio salón con techos altos. Es el centro de reunión principal del castillo."
        )
        
        library = await self.memory_system.create_location(
            "Biblioteca Colaborativa", 
            "Una vasta biblioteca donde los jugadores pueden compartir conocimiento."
        )
        
        kitchen = await self.memory_system.create_location(
            "Cocina Comunitaria",
            "Una cocina donde los jugadores pueden preparar objetos juntos."
        )
        
        throne_room = await self.memory_system.create_location(
            "Sala del Trono",
            "La sala más importante del castillo, reservada para administradores."
        )
        
        # Ahora actualizar las conexiones con los IDs reales
        logger.info("🔗 Actualizando conexiones entre ubicaciones...")
        
        try:
            await self.memory_system.update_location_connections(
                str(entrance.id),
                {"norte": str(hall.id)}
            )
            logger.info(f"✅ Conexiones actualizadas para entrada: {entrance.id}")
            
            await self.memory_system.update_location_connections(
                str(hall.id),
                {
                    "sur": str(entrance.id),
                    "este": str(library.id),
                    "oeste": str(kitchen.id),
                    "norte": str(throne_room.id)
                }
            )
            logger.info(f"✅ Conexiones actualizadas para hall: {hall.id}")
            
            await self.memory_system.update_location_connections(
                str(library.id),
                {"oeste": str(hall.id)}
            )
            logger.info(f"✅ Conexiones actualizadas para biblioteca: {library.id}")
            
            await self.memory_system.update_location_connections(
                str(kitchen.id),
                {"este": str(hall.id)}
            )
            logger.info(f"✅ Conexiones actualizadas para cocina: {kitchen.id}")
            
            await self.memory_system.update_location_connections(
                str(throne_room.id),
                {"sur": str(hall.id)}
            )
            logger.info(f"✅ Conexiones actualizadas para sala del trono: {throne_room.id}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando conexiones: {e}")
            raise
        
        # Crear objetos iniciales
        await self.memory_system.create_object(
            "Llave Maestra Compartida",
            "Una llave dorada que puede ser usada por cualquier jugador",
            str(entrance.id),
            properties={"type": "key", "shareable": True, "magical": True}
        )
        
        await self.memory_system.create_object(
            "Libro de Registro de Aventureros",
            "Un libro donde se registran todos los jugadores que pasan por aquí",
            str(library.id),
            properties={"type": "book", "interactive": True, "records": []}
        )
        
        await self.memory_system.create_object(
            "Mesa de Crafting Colaborativa",
            "Una mesa donde múltiples jugadores pueden trabajar juntos",
            str(kitchen.id),
            properties={"type": "crafting_table", "multi_user": True, "recipes": []}
        )
        
        # Establecer ubicación inicial para nuevos jugadores
        self.default_spawn_location = str(entrance.id)
        
        # Registrar evento de creación del mundo
        await self.memory_system._record_event(
            event_type="world_creation",
            actor="system",
            action="created multiplayer world",
            target=None,  # No hay un target específico para la creación del mundo
            location_id=str(entrance.id),  # Usar la entrada como ubicación de referencia
            context={
                "locations_created": 5,
                "objects_created": 3,
                "world_type": "multiplayer_default"
            }
        )
    
    async def connect_player(self, username: str, role: PlayerRole = PlayerRole.PLAYER,
                           websocket_connection=None) -> tuple[str, str, Dict]:
        """
        Conecta un jugador al juego multi-jugador
        
        Returns:
            tuple: (player_id, session_id, initial_game_state)
        """
        try:
            # Asegurar que el mundo está inicializado
            if not self.game_state["world_initialized"]:
                await self.initialize_world()
            
            # Conectar jugador
            player_id, session_id = await self.session_manager.connect_player(
                username, role, websocket_connection
            )
            
            # Establecer ubicación inicial
            player = self.session_manager.players[player_id]
            player.current_location = self.default_spawn_location
            
            # Obtener estado inicial del juego para el jugador
            initial_state = await self._get_initial_game_state(player_id)
            
            # Registrar conexión en el sistema de memoria
            await self.memory_system._record_event(
                event_type="player_connect",
                actor=f"player_{player_id}",
                action=f"connected as {username}",
                location_id=self.default_spawn_location,
                context={
                    "username": username,
                    "role": role.value,
                    "session_id": session_id
                }
            )
            
            logger.info(f"🎮 Jugador {username} conectado al mundo multi-jugador")
            
            return player_id, session_id, initial_state
            
        except Exception as e:
            logger.error(f"❌ Error conectando jugador {username}: {e}")
            raise
    
    async def disconnect_player(self, player_id: str) -> bool:
        """Desconecta un jugador del juego"""
        try:
            player = self.session_manager.players.get(player_id)
            if player:
                # Registrar desconexión
                await self.memory_system._record_event(
                    event_type="player_disconnect",
                    actor=f"player_{player_id}",
                    action=f"disconnected {player.username}",
                    context={"username": player.username}
                )
            
            # Desconectar del session manager
            success = await self.session_manager.disconnect_player(player_id)
            
            if success:
                logger.info(f"👋 Jugador {player.username if player else player_id} desconectado")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error desconectando jugador {player_id}: {e}")
            return False
    
    async def process_player_command(self, player_id: str, command: str) -> Dict:
        """
        Procesa un comando de jugador y devuelve el resultado
        
        Args:
            player_id: ID del jugador
            command: Comando en lenguaje natural
            
        Returns:
            Dict con resultado del comando
        """
        try:
            player = self.session_manager.players.get(player_id)
            if not player:
                return {"success": False, "error": "Jugador no encontrado"}
            
            # Parsear comando básico
            action_data = self._parse_command(command)
            
            # Procesar acción a través del sincronizador
            result = await self.world_synchronizer.apply_player_action(
                player_id, action_data["action_type"], action_data
            )
            
            # Agregar información del contexto multi-jugador
            if result["success"]:
                result["multiplayer_context"] = await self._get_multiplayer_context(player_id)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error procesando comando '{command}' de {player_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Error procesando comando: {e}"
            }
    
    def _parse_command(self, command: str) -> Dict:
        """Parsea un comando en lenguaje natural a acción estructurada"""
        command = command.lower().strip()
        
        # Comandos de movimiento
        if any(word in command for word in ["ir", "mover", "caminar"]):
            for direction in ["norte", "sur", "este", "oeste"]:
                if direction in command:
                    return {
                        "action_type": "move",
                        "direction": direction,
                        "description": f"moverse hacia {direction}"
                    }
        
        # Comandos de objeto
        elif any(word in command for word in ["tomar", "coger", "agarrar"]):
            object_name = command.replace("tomar", "").replace("coger", "").replace("agarrar", "").strip()
            return {
                "action_type": "take",
                "object_name": object_name,
                "description": f"tomar {object_name}"
            }
        
        elif any(word in command for word in ["dejar", "soltar", "tirar"]):
            object_name = command.replace("dejar", "").replace("soltar", "").replace("tirar", "").strip()
            return {
                "action_type": "drop",
                "object_name": object_name,
                "description": f"dejar {object_name}"
            }
        
        # Comandos de observación
        elif any(word in command for word in ["mirar", "ver", "observar", "examinar"]):
            return {
                "action_type": "look",
                "description": "mirar alrededor"
            }
        
        # Chat
        elif command.startswith("decir ") or command.startswith("say "):
            message = command.replace("decir ", "").replace("say ", "")
            return {
                "action_type": "say",
                "message": message,
                "description": f"decir: {message}"
            }
        
        # Comando genérico
        else:
            return {
                "action_type": "generic",
                "command": command,
                "description": command
            }
    
    async def _get_initial_game_state(self, player_id: str) -> Dict:
        """Obtiene el estado inicial del juego para un jugador"""
        player = self.session_manager.players[player_id]
        
        # Obtener ubicación inicial
        location = await self.memory_system.get_location(player.current_location)
        objects = await self.memory_system.get_objects_in_location(player.current_location)
        other_players = self.session_manager.get_players_in_location(player.current_location)
        other_players = [p for p in other_players if p.id != player_id]
        
        return {
            "player": player.to_dict(),
            "current_location": {
                "id": player.current_location,
                "name": location["name"],
                "description": location["description"],
                "connections": location.get("connections", {})
            },
            "objects_here": [
                {"id": obj["id"], "name": obj["name"], "description": obj["description"]}
                for obj in objects
            ],
            "other_players": [
                {"username": p.username, "role": p.role.value}
                for p in other_players
            ],
            "session_info": self.session_manager.get_session_stats(),
            "welcome_message": f"¡Bienvenido al mundo multi-jugador, {player.username}!"
        }
    
    async def _get_multiplayer_context(self, player_id: str) -> Dict:
        """Obtiene contexto multi-jugador para agregar a respuestas"""
        player = self.session_manager.players[player_id]
        other_players = self.session_manager.get_players_in_location(player.current_location)
        other_players = [p for p in other_players if p.id != player_id]
        
        return {
            "other_players_here": [p.username for p in other_players],
            "total_online_players": len(self.session_manager.get_online_players()),
            "your_role": player.role.value
        }
    
    async def broadcast_server_event(self, event_type: str, data: Dict):
        """Envía un evento del servidor a todos los jugadores"""
        await self.session_manager.broadcast_world_event(f"server_{event_type}", data)
    
    def get_server_stats(self) -> Dict:
        """Obtiene estadísticas completas del servidor"""
        return {
            "server_info": {
                "started_at": self.game_state["server_started"].isoformat(),
                "uptime_seconds": (datetime.now() - self.game_state["server_started"]).total_seconds(),
                "world_initialized": self.game_state["world_initialized"]
            },
            "session_stats": self.session_manager.get_session_stats(),
            "world_stats": self.world_synchronizer.get_world_state(),
            "memory_stats": {
                "database_path": self.memory_system.db_path,
                # Agregar más estadísticas de memoria si están disponibles
            }
        }

# Instancia global del gestor de juego multi-jugador
multiplayer_game = None

def get_multiplayer_game(memory_db_path: str = "multiplayer_world.db", 
                        max_players: int = 10) -> MultiPlayerGameManager:
    """Obtiene o crea la instancia global del juego multi-jugador"""
    global multiplayer_game
    if multiplayer_game is None:
        multiplayer_game = MultiPlayerGameManager(memory_db_path, max_players)
    return multiplayer_game

# Test del sistema completo
async def test_multiplayer_game():
    """Test completo del sistema multi-jugador"""
    print("🧪 TESTING SISTEMA COMPLETO MULTI-JUGADOR")
    print("=" * 60)
    
    try:
        # Crear instancia del juego
        game = MultiPlayerGameManager("test_multiplayer.db", max_players=5)
        await game.initialize_world()
        
        # Conectar jugadores
        alice_id, alice_session, alice_state = await game.connect_player("Alice", PlayerRole.ADMIN)
        print(f"✅ Alice conectada como ADMIN")
        
        bob_id, bob_session, bob_state = await game.connect_player("Bob", PlayerRole.PLAYER)
        print(f"✅ Bob conectado como PLAYER")
        
        # Probar comandos
        print(f"\n🎮 TESTING COMANDOS:")
        
        # Alice mira alrededor
        result = await game.process_player_command(alice_id, "mirar alrededor")
        print(f"   Alice mira: {result['success']}")
        
        # Bob se mueve al norte
        result = await game.process_player_command(bob_id, "ir norte")
        print(f"   Bob va norte: {result['success']}")
        
        # Alice toma la llave
        result = await game.process_player_command(alice_id, "tomar llave")
        print(f"   Alice toma llave: {result['success']}")
        
        # Chat
        result = await game.process_player_command(alice_id, "decir Hola Bob!")
        print(f"   Alice dice hola: {result['success']}")
        
        # Estadísticas finales
        stats = game.get_server_stats()
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Jugadores online: {stats['session_stats']['online_players']}")
        print(f"   Mundo inicializado: {stats['server_info']['world_initialized']}")
        
        print(f"\n🎉 Test multi-jugador completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_multiplayer_game())
