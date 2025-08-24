# 🔌 WEBSOCKET HANDLER MULTI-JUGADOR

"""
Manejador de WebSocket para Comunicación Multi-jugador
=====================================================

Gestiona las conexiones WebSocket de múltiples jugadores,
comunicación en tiempo real, y eventos del juego.
"""

import asyncio
import json
import logging
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

from .multiplayer_game import MultiPlayerGameManager, get_multiplayer_game
from .session_manager import PlayerRole

logger = logging.getLogger(__name__)

class MultiPlayerWebSocketManager:
    """
    Gestor de WebSocket para Multi-jugador
    
    Maneja todas las conexiones WebSocket de jugadores,
    autenticación, y comunicación en tiempo real.
    """
    
    def __init__(self):
        # Conexiones activas: websocket_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # Mapeo de jugador a WebSocket: player_id -> websocket_id
        self.player_connections: Dict[str, str] = {}
        # Salas de chat: location_id -> Set[player_id]
        self.location_rooms: Dict[str, Set[str]] = {}
        
        # Referencia al juego multi-jugador
        self.game: MultiPlayerGameManager = get_multiplayer_game()
        
        logger.info("🔌 MultiPlayerWebSocketManager inicializado")
    
    async def connect(self, websocket: WebSocket, player_id: str = None):
        """Conecta un nuevo WebSocket"""
        await websocket.accept()
        
        websocket_id = f"ws_{id(websocket)}_{datetime.now().timestamp()}"
        self.active_connections[websocket_id] = websocket
        
        logger.info(f"🔌 Nueva conexión WebSocket: {websocket_id}")
        
        # Enviar mensaje de bienvenida
        await self.send_personal_message(websocket, {
            "type": "connection_established",
            "websocket_id": websocket_id,
            "message": "Conexión WebSocket establecida. Esperando autenticación..."
        })
        
        return websocket_id
    
    async def disconnect(self, websocket_id: str):
        """Desconecta un WebSocket"""
        if websocket_id in self.active_connections:
            del self.active_connections[websocket_id]
        
        # Encontrar y desconectar jugador asociado
        player_id = None
        for pid, ws_id in self.player_connections.items():
            if ws_id == websocket_id:
                player_id = pid
                break
        
        if player_id:
            await self.disconnect_player(player_id)
        
        logger.info(f"🔌 WebSocket desconectado: {websocket_id}")
    
    async def authenticate_player(self, websocket_id: str, username: str, 
                                role: str = "player") -> Dict:
        """Autentica un jugador en el sistema multi-jugador"""
        try:
            websocket = self.active_connections.get(websocket_id)
            if not websocket:
                return {"success": False, "error": "WebSocket no encontrado"}
            
            # Convertir rol string a enum
            player_role = PlayerRole.PLAYER
            if role.lower() == "admin":
                player_role = PlayerRole.ADMIN
            elif role.lower() == "observer":
                player_role = PlayerRole.OBSERVER
            
            # Conectar jugador al juego
            player_id, session_id, initial_state = await self.game.connect_player(
                username, player_role, websocket
            )
            
            # Asociar WebSocket con jugador
            self.player_connections[player_id] = websocket_id
            
            # Agregar a sala de ubicación
            location_id = initial_state["current_location"]["id"]
            if location_id not in self.location_rooms:
                self.location_rooms[location_id] = set()
            self.location_rooms[location_id].add(player_id)
            
            # Enviar estado inicial
            await self.send_personal_message(websocket, {
                "type": "authentication_success",
                "player_id": player_id,
                "session_id": session_id,
                "initial_state": initial_state
            })
            
            # Notificar a otros jugadores en la misma ubicación
            await self.broadcast_to_location(location_id, {
                "type": "player_joined_location",
                "player": {
                    "id": player_id,
                    "username": username,
                    "role": role
                },
                "message": f"🎮 {username} ha llegado a {initial_state['current_location']['name']}"
            }, exclude_player=player_id)
            
            logger.info(f"✅ Jugador autenticado: {username} ({player_id})")
            
            return {
                "success": True,
                "player_id": player_id,
                "session_id": session_id,
                "message": f"Bienvenido al mundo multi-jugador, {username}!"
            }
            
        except Exception as e:
            logger.error(f"❌ Error autenticando jugador {username}: {e}")
            return {"success": False, "error": str(e)}
    
    async def disconnect_player(self, player_id: str):
        """Desconecta un jugador del juego"""
        try:
            # Remover de sala de ubicación
            player = self.game.session_manager.players.get(player_id)
            if player and player.current_location:
                location_id = player.current_location
                if location_id in self.location_rooms:
                    self.location_rooms[location_id].discard(player_id)
                
                # Notificar a otros jugadores
                await self.broadcast_to_location(location_id, {
                    "type": "player_left_location",
                    "player": player.to_dict(),
                    "message": f"👋 {player.username} ha salido del juego"
                }, exclude_player=player_id)
            
            # Desconectar del juego
            await self.game.disconnect_player(player_id)
            
            # Remover mapeo de conexión
            if player_id in self.player_connections:
                del self.player_connections[player_id]
                
        except Exception as e:
            logger.error(f"❌ Error desconectando jugador {player_id}: {e}")
    
    async def process_player_message(self, websocket_id: str, message: Dict) -> Dict:
        """Procesa un mensaje de jugador"""
        try:
            # Encontrar jugador por WebSocket
            player_id = None
            for pid, ws_id in self.player_connections.items():
                if ws_id == websocket_id:
                    player_id = pid
                    break
            
            if not player_id:
                return {"success": False, "error": "Jugador no autenticado"}
            
            message_type = message.get("type", "")
            
            if message_type == "game_command":
                return await self._handle_game_command(player_id, message)
            
            elif message_type == "chat_message":
                return await self._handle_chat_message(player_id, message)
            
            elif message_type == "ping":
                return await self._handle_ping(player_id, message)
            
            elif message_type == "get_status":
                return await self._handle_get_status(player_id, message)
            
            else:
                return {"success": False, "error": f"Tipo de mensaje no reconocido: {message_type}"}
                
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_game_command(self, player_id: str, message: Dict) -> Dict:
        """Maneja comandos del juego"""
        command = message.get("command", "")
        
        # Procesar comando a través del juego
        result = await self.game.process_player_command(player_id, command)
        
        # Si el jugador se movió, actualizar salas
        if result.get("success") and result.get("location_id"):
            await self._update_player_location(player_id, result["location_id"])
        
        return result
    
    async def _handle_chat_message(self, player_id: str, message: Dict) -> Dict:
        """Maneja mensajes de chat"""
        chat_message = message.get("message", "")
        player = self.game.session_manager.players.get(player_id)
        
        if not player:
            return {"success": False, "error": "Jugador no encontrado"}
        
        # Broadcast del mensaje a la ubicación
        await self.broadcast_to_location(player.current_location, {
            "type": "chat_message",
            "from_player": {
                "id": player_id,
                "username": player.username,
                "role": player.role.value
            },
            "message": chat_message,
            "timestamp": datetime.now().isoformat()
        }, exclude_player=player_id)
        
        return {"success": True, "message": "Mensaje enviado"}
    
    async def _handle_ping(self, player_id: str, message: Dict) -> Dict:
        """Maneja ping para mantener conexión viva"""
        return {
            "success": True, 
            "type": "pong",
            "timestamp": datetime.now().isoformat(),
            "player_id": player_id
        }
    
    async def _handle_get_status(self, player_id: str, message: Dict) -> Dict:
        """Obtiene estado actual del jugador y juego"""
        player = self.game.session_manager.players.get(player_id)
        if not player:
            return {"success": False, "error": "Jugador no encontrado"}
        
        # Obtener estado completo
        stats = self.game.get_server_stats()
        location_info = await self.game.memory_system.get_location(player.current_location)
        other_players = self.game.session_manager.get_players_in_location(player.current_location)
        other_players = [p for p in other_players if p.id != player_id]
        
        return {
            "success": True,
            "status": {
                "player": player.to_dict(),
                "current_location": location_info,
                "other_players_here": [p.username for p in other_players],
                "server_stats": stats
            }
        }
    
    async def _update_player_location(self, player_id: str, new_location_id: str):
        """Actualiza la ubicación de un jugador en las salas"""
        player = self.game.session_manager.players.get(player_id)
        if not player:
            return
        
        old_location = player.current_location
        
        # Remover de sala anterior
        if old_location and old_location in self.location_rooms:
            self.location_rooms[old_location].discard(player_id)
            
            # Notificar salida
            await self.broadcast_to_location(old_location, {
                "type": "player_left_location",
                "player": player.to_dict(),
                "message": f"👋 {player.username} se ha ido"
            }, exclude_player=player_id)
        
        # Agregar a nueva sala
        if new_location_id not in self.location_rooms:
            self.location_rooms[new_location_id] = set()
        self.location_rooms[new_location_id].add(player_id)
        
        # Notificar llegada
        await self.broadcast_to_location(new_location_id, {
            "type": "player_joined_location", 
            "player": player.to_dict(),
            "message": f"🎮 {player.username} ha llegado"
        }, exclude_player=player_id)
    
    async def broadcast_to_location(self, location_id: str, message: Dict, exclude_player: str = None):
        """Envía mensaje a todos los jugadores en una ubicación"""
        if location_id not in self.location_rooms:
            return
        
        for player_id in self.location_rooms[location_id]:
            if player_id != exclude_player:
                await self.send_to_player(player_id, message)
    
    async def send_to_player(self, player_id: str, message: Dict):
        """Envía mensaje a un jugador específico"""
        websocket_id = self.player_connections.get(player_id)
        if websocket_id and websocket_id in self.active_connections:
            websocket = self.active_connections[websocket_id]
            await self.send_personal_message(websocket, message)
    
    async def send_personal_message(self, websocket: WebSocket, message: Dict):
        """Envía mensaje personal a un WebSocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"❌ Error enviando mensaje personal: {e}")
    
    async def broadcast_to_all(self, message: Dict):
        """Envía mensaje a todos los jugadores conectados"""
        for websocket in self.active_connections.values():
            await self.send_personal_message(websocket, message)
    
    def get_connection_stats(self) -> Dict:
        """Obtiene estadísticas de conexiones"""
        return {
            "total_connections": len(self.active_connections),
            "authenticated_players": len(self.player_connections),
            "location_rooms": {
                loc_id: len(players) for loc_id, players in self.location_rooms.items()
            },
            "server_stats": self.game.get_server_stats()
        }

# Instancia global del gestor de WebSocket
websocket_manager = MultiPlayerWebSocketManager()

# Endpoint principal para WebSocket
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint principal para conexiones WebSocket multi-jugador"""
    websocket_id = await websocket_manager.connect(websocket)
    
    try:
        while True:
            # Recibir mensaje
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Procesar mensaje
            response = await websocket_manager.process_player_message(websocket_id, message)
            
            # Enviar respuesta
            await websocket_manager.send_personal_message(websocket, {
                "type": "response",
                "original_message": message,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket_id)
    except Exception as e:
        logger.error(f"❌ Error en WebSocket {websocket_id}: {e}")
        await websocket_manager.disconnect(websocket_id)
