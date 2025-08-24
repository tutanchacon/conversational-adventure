# 👥 SISTEMA MULTI-JUGADOR - ADVENTURE GAME v3.0

"""
Sistema de Multi-jugador en Tiempo Real
========================================

Gestiona múltiples jugadores simultáneos en el mismo mundo compartido.
Sincronización en tiempo real de acciones, chat, y estado del mundo.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerRole(Enum):
    """Roles de jugador en el sistema multi-jugador"""
    ADMIN = "admin"          # Control total del mundo
    PLAYER = "player"        # Jugador estándar
    OBSERVER = "observer"    # Solo observa, no puede actuar

class PlayerStatus(Enum):
    """Estados de conexión del jugador"""
    ONLINE = "online"
    IDLE = "idle"
    OFFLINE = "offline"

@dataclass
class Player:
    """Representa un jugador en el sistema multi-jugador"""
    id: str
    username: str
    role: PlayerRole
    status: PlayerStatus
    current_location: Optional[str] = None
    connected_at: Optional[datetime] = None
    last_action: Optional[datetime] = None
    session_id: Optional[str] = None
    websocket_connection = None
    
    def to_dict(self) -> dict:
        """Convierte el jugador a diccionario para JSON"""
        data = asdict(self)
        # Convertir enums a strings
        data['role'] = self.role.value
        data['status'] = self.status.value
        # Convertir datetime a ISO string
        if self.connected_at:
            data['connected_at'] = self.connected_at.isoformat()
        if self.last_action:
            data['last_action'] = self.last_action.isoformat()
        # Remover websocket (no serializable)
        data.pop('websocket_connection', None)
        return data

class MultiPlayerSessionManager:
    """
    Gestor de Sesiones Multi-jugador
    
    Maneja la conexión, autenticación y estado de múltiples jugadores
    en el mismo mundo compartido del Adventure Game.
    """
    
    def __init__(self, max_players: int = 10):
        self.max_players = max_players
        self.players: Dict[str, Player] = {}  # player_id -> Player
        self.active_sessions: Dict[str, str] = {}  # session_id -> player_id
        self.world_state_lock = asyncio.Lock()
        self.broadcast_callbacks: List = []
        
        logger.info(f"🎮 MultiPlayerSessionManager inicializado (max: {max_players} jugadores)")
    
    async def connect_player(self, username: str, role: PlayerRole = PlayerRole.PLAYER, 
                           websocket_connection=None) -> tuple[str, str]:
        """
        Conecta un nuevo jugador al sistema multi-jugador
        
        Returns:
            tuple: (player_id, session_id)
        """
        async with self.world_state_lock:
            # Verificar límite de jugadores
            if len([p for p in self.players.values() if p.status == PlayerStatus.ONLINE]) >= self.max_players:
                raise Exception(f"❌ Servidor lleno. Máximo {self.max_players} jugadores.")
            
            # Verificar si el username ya existe
            existing_player = self.get_player_by_username(username)
            if existing_player and existing_player.status == PlayerStatus.ONLINE:
                raise Exception(f"❌ Usuario '{username}' ya está conectado.")
            
            # Crear o actualizar jugador
            if existing_player:
                # Reconexión de jugador existente
                player_id = existing_player.id
                existing_player.status = PlayerStatus.ONLINE
                existing_player.connected_at = datetime.now()
                existing_player.websocket_connection = websocket_connection
                logger.info(f"🔄 Jugador reconectado: {username} ({player_id})")
            else:
                # Nuevo jugador
                player_id = str(uuid.uuid4())
                new_player = Player(
                    id=player_id,
                    username=username,
                    role=role,
                    status=PlayerStatus.ONLINE,
                    connected_at=datetime.now(),
                    websocket_connection=websocket_connection
                )
                self.players[player_id] = new_player
                logger.info(f"✅ Nuevo jugador conectado: {username} ({player_id}) - Rol: {role.value}")
            
            # Crear sesión
            session_id = str(uuid.uuid4())
            self.active_sessions[session_id] = player_id
            self.players[player_id].session_id = session_id
            
            # Notificar a otros jugadores
            await self.broadcast_player_event("player_joined", {
                "player": self.players[player_id].to_dict(),
                "message": f"🎮 {username} se ha unido al juego"
            }, exclude_player=player_id)
            
            return player_id, session_id
    
    async def disconnect_player(self, player_id: str) -> bool:
        """Desconecta un jugador del sistema"""
        async with self.world_state_lock:
            if player_id not in self.players:
                return False
            
            player = self.players[player_id]
            username = player.username
            
            # Cambiar estado a offline
            player.status = PlayerStatus.OFFLINE
            player.websocket_connection = None
            
            # Remover sesión activa
            if player.session_id in self.active_sessions:
                del self.active_sessions[player.session_id]
            
            # Notificar a otros jugadores
            await self.broadcast_player_event("player_left", {
                "player": player.to_dict(),
                "message": f"👋 {username} ha salido del juego"
            }, exclude_player=player_id)
            
            logger.info(f"👋 Jugador desconectado: {username} ({player_id})")
            return True
    
    async def update_player_action(self, player_id: str, action: str, location: str = None):
        """Actualiza la última acción de un jugador"""
        if player_id in self.players:
            player = self.players[player_id]
            player.last_action = datetime.now()
            if location:
                player.current_location = location
            
            # Broadcast de la acción a otros jugadores
            await self.broadcast_player_event("player_action", {
                "player_id": player_id,
                "username": player.username,
                "action": action,
                "location": location,
                "timestamp": player.last_action.isoformat()
            }, exclude_player=player_id)
    
    def get_player_by_username(self, username: str) -> Optional[Player]:
        """Busca un jugador por username"""
        for player in self.players.values():
            if player.username == username:
                return player
        return None
    
    def get_player_by_session(self, session_id: str) -> Optional[Player]:
        """Obtiene un jugador por session_id"""
        player_id = self.active_sessions.get(session_id)
        if player_id:
            return self.players.get(player_id)
        return None
    
    def get_online_players(self) -> List[Player]:
        """Obtiene lista de jugadores online"""
        return [player for player in self.players.values() if player.status == PlayerStatus.ONLINE]
    
    def get_players_in_location(self, location_id: str) -> List[Player]:
        """Obtiene jugadores en una ubicación específica"""
        return [
            player for player in self.players.values() 
            if player.current_location == location_id and player.status == PlayerStatus.ONLINE
        ]
    
    async def broadcast_player_event(self, event_type: str, data: dict, exclude_player: str = None):
        """Envía un evento a todos los jugadores conectados"""
        message = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Enviar a todos los jugadores online excepto el excluido
        for player in self.get_online_players():
            if player.id != exclude_player and player.websocket_connection:
                try:
                    await player.websocket_connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"❌ Error enviando mensaje a {player.username}: {e}")
    
    async def broadcast_world_event(self, event_type: str, data: dict):
        """Envía un evento global del mundo a todos los jugadores"""
        message = {
            "type": "world_event",
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        for player in self.get_online_players():
            if player.websocket_connection:
                try:
                    await player.websocket_connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"❌ Error enviando evento mundial a {player.username}: {e}")
    
    def get_session_stats(self) -> dict:
        """Obtiene estadísticas de las sesiones activas"""
        online_players = self.get_online_players()
        return {
            "total_players": len(self.players),
            "online_players": len(online_players),
            "max_players": self.max_players,
            "active_sessions": len(self.active_sessions),
            "players_by_role": {
                role.value: len([p for p in online_players if p.role == role])
                for role in PlayerRole
            },
            "server_load": f"{len(online_players)}/{self.max_players}",
            "server_load_percent": round((len(online_players) / self.max_players) * 100, 1)
        }
    
    def to_dict(self) -> dict:
        """Convierte el estado completo a diccionario"""
        return {
            "players": {pid: player.to_dict() for pid, player in self.players.items()},
            "active_sessions": len(self.active_sessions),
            "stats": self.get_session_stats()
        }

# Instancia global del gestor de sesiones
session_manager = MultiPlayerSessionManager()

# Ejemplo de uso y testing
async def test_multiplayer_system():
    """Función de prueba del sistema multi-jugador"""
    print("🧪 TESTING SISTEMA MULTI-JUGADOR")
    print("=" * 50)
    
    # Conectar jugadores de prueba
    try:
        player1_id, session1 = await session_manager.connect_player("Alice", PlayerRole.ADMIN)
        print(f"✅ Alice conectada: {player1_id}")
        
        player2_id, session2 = await session_manager.connect_player("Bob", PlayerRole.PLAYER)
        print(f"✅ Bob conectado: {player2_id}")
        
        player3_id, session3 = await session_manager.connect_player("Charlie", PlayerRole.OBSERVER)
        print(f"✅ Charlie conectado: {player3_id}")
        
        # Actualizar acciones
        await session_manager.update_player_action(player1_id, "mirar alrededor", "entrada_castillo")
        await session_manager.update_player_action(player2_id, "tomar llave", "entrada_castillo")
        
        # Mostrar estadísticas
        stats = session_manager.get_session_stats()
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   Jugadores online: {stats['online_players']}/{stats['max_players']}")
        print(f"   Carga del servidor: {stats['server_load_percent']}%")
        print(f"   Por roles: {stats['players_by_role']}")
        
        # Mostrar jugadores online
        print(f"\n👥 JUGADORES ONLINE:")
        for player in session_manager.get_online_players():
            print(f"   • {player.username} ({player.role.value}) - {player.current_location or 'Sin ubicación'}")
        
        # Desconectar un jugador
        await session_manager.disconnect_player(player2_id)
        print(f"\n👋 Bob desconectado")
        
        # Estadísticas finales
        final_stats = session_manager.get_session_stats()
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Jugadores online: {final_stats['online_players']}/{final_stats['max_players']}")
        
        print("\n🎉 Test completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")

if __name__ == "__main__":
    # Ejecutar test
    asyncio.run(test_multiplayer_system())
