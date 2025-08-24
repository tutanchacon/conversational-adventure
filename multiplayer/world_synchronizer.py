# 🌍 WORLD SYNCHRONIZER - ESTADO COMPARTIDO

"""
Sincronizador de Estado del Mundo Multi-jugador
===============================================

Mantiene el estado del mundo sincronizado entre todos los jugadores.
Gestiona cambios concurrentes y resuelve conflictos automáticamente.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class WorldChange:
    """Representa un cambio en el estado del mundo"""
    change_id: str
    player_id: str
    change_type: str  # "move_object", "create_object", "delete_object", "modify_object", "player_move"
    target_id: str  # ID del objeto/ubicación afectada
    old_state: Optional[Dict] = None
    new_state: Optional[Dict] = None
    timestamp: Optional[datetime] = None
    synchronized: bool = False

class WorldSynchronizer:
    """
    Sincronizador de Estado del Mundo Multi-jugador
    
    Mantiene consistencia del estado del mundo entre múltiples jugadores,
    gestiona cambios concurrentes y propaga actualizaciones en tiempo real.
    """
    
    def __init__(self, memory_system, session_manager):
        self.memory_system = memory_system
        self.session_manager = session_manager
        self.pending_changes: List[WorldChange] = []
        self.sync_lock = asyncio.Lock()
        self.change_history: List[WorldChange] = []
        
        # Callbacks para diferentes tipos de cambios
        self.change_callbacks = {
            "object_moved": [],
            "object_created": [],
            "object_modified": [],
            "player_moved": [],
            "world_event": []
        }
        
        logger.info("🌍 WorldSynchronizer inicializado")
    
    async def apply_player_action(self, player_id: str, action_type: str, 
                                action_data: Dict) -> Dict:
        """
        Aplica una acción de jugador y sincroniza con otros jugadores
        
        Args:
            player_id: ID del jugador que ejecuta la acción
            action_type: Tipo de acción ("move", "take", "drop", "use", etc.)
            action_data: Datos específicos de la acción
            
        Returns:
            Dict con resultado de la acción y cambios aplicados
        """
        async with self.sync_lock:
            try:
                result = await self._execute_action(player_id, action_type, action_data)
                
                if result["success"]:
                    # Crear cambio en el mundo
                    change = WorldChange(
                        change_id=f"{player_id}_{datetime.now().timestamp()}",
                        player_id=player_id,
                        change_type=action_type,
                        target_id=action_data.get("target_id", ""),
                        old_state=action_data.get("old_state"),
                        new_state=result.get("new_state"),
                        timestamp=datetime.now()
                    )
                    
                    # Aplicar cambio
                    await self._apply_world_change(change)
                    
                    # Sincronizar con otros jugadores
                    await self._broadcast_world_change(change, result)
                    
                    # Actualizar acción del jugador
                    await self.session_manager.update_player_action(
                        player_id, 
                        f"{action_type}: {action_data.get('description', '')}"
                    )
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Error aplicando acción {action_type} de {player_id}: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Error ejecutando acción: {e}"
                }
    
    async def _execute_action(self, player_id: str, action_type: str, 
                            action_data: Dict) -> Dict:
        """Ejecuta una acción específica en el sistema de memoria"""
        
        player = self.session_manager.players.get(player_id)
        if not player:
            return {"success": False, "error": "Jugador no encontrado"}
        
        # Obtener ubicación actual del jugador
        current_location = player.current_location
        
        if action_type == "move":
            return await self._handle_player_move(player_id, action_data)
        
        elif action_type == "take":
            return await self._handle_take_object(player_id, action_data, current_location)
        
        elif action_type == "drop":
            return await self._handle_drop_object(player_id, action_data, current_location)
        
        elif action_type == "look":
            return await self._handle_look_around(player_id, current_location)
        
        elif action_type == "use":
            return await self._handle_use_object(player_id, action_data)
        
        elif action_type == "say":
            return await self._handle_player_chat(player_id, action_data)
        
        else:
            return {
                "success": False, 
                "error": f"Acción '{action_type}' no reconocida"
            }
    
    async def _handle_player_move(self, player_id: str, action_data: Dict) -> Dict:
        """Maneja movimiento de jugador"""
        direction = action_data.get("direction")
        player = self.session_manager.players[player_id]
        
        try:
            # Obtener ubicación actual
            current_location_id = player.current_location
            if not current_location_id:
                return {"success": False, "error": "Jugador no tiene ubicación actual"}
            
            # Obtener ubicaciones y conexiones del sistema de memoria
            current_location = await self.memory_system.get_location(current_location_id)
            connections = current_location.get("connections", {})
            
            if direction not in connections:
                return {
                    "success": False, 
                    "error": f"No puedes ir hacia {direction} desde aquí",
                    "message": f"Direcciones disponibles: {', '.join(connections.keys())}"
                }
            
            new_location_id = connections[direction]
            new_location = await self.memory_system.get_location(new_location_id)
            
            # Actualizar ubicación del jugador
            player.current_location = new_location_id
            
            # Registrar evento en memoria
            await self.memory_system._record_event(
                event_type="player_move",
                actor=f"player_{player_id}",
                action=f"moved {direction}",
                location_id=new_location_id,
                context={
                    "from_location": current_location_id,
                    "to_location": new_location_id,
                    "direction": direction,
                    "player_name": player.username
                }
            )
            
            # Obtener jugadores en la nueva ubicación
            other_players = self.session_manager.get_players_in_location(new_location_id)
            other_players = [p for p in other_players if p.id != player_id]
            
            return {
                "success": True,
                "message": f"Te mueves hacia {direction} y llegas a {new_location['name']}",
                "new_state": {
                    "location": new_location,
                    "other_players": [p.username for p in other_players]
                },
                "location_id": new_location_id,
                "player_moved": True
            }
            
        except Exception as e:
            logger.error(f"Error en movimiento: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_take_object(self, player_id: str, action_data: Dict, 
                                current_location: str) -> Dict:
        """Maneja tomar un objeto"""
        object_name = action_data.get("object_name", "").lower()
        
        try:
            # Buscar objeto en la ubicación actual
            objects = await self.memory_system.get_objects_in_location(current_location)
            target_object = None
            
            for obj in objects:
                if object_name in obj["name"].lower():
                    target_object = obj
                    break
            
            if not target_object:
                return {
                    "success": False,
                    "error": f"No encuentras '{object_name}' aquí",
                    "message": f"Objetos disponibles: {', '.join([obj['name'] for obj in objects])}"
                }
            
            # Mover objeto al inventario del jugador (ubicación especial)
            player_inventory_id = f"inventory_{player_id}"
            
            # Asegurar que existe la ubicación del inventario
            try:
                await self.memory_system.get_location(player_inventory_id)
            except:
                await self.memory_system.create_location(
                    f"Inventario de {self.session_manager.players[player_id].username}",
                    f"Inventario personal del jugador",
                    location_id=player_inventory_id
                )
            
            # Mover objeto
            await self.memory_system.move_object(
                target_object["id"], 
                player_inventory_id,
                actor=f"player_{player_id}"
            )
            
            return {
                "success": True,
                "message": f"Tomas {target_object['name']}",
                "new_state": {
                    "object_moved": True,
                    "object": target_object,
                    "from_location": current_location,
                    "to_location": player_inventory_id
                }
            }
            
        except Exception as e:
            logger.error(f"Error tomando objeto: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_drop_object(self, player_id: str, action_data: Dict, 
                                current_location: str) -> Dict:
        """Maneja soltar un objeto"""
        object_name = action_data.get("object_name", "").lower()
        player_inventory_id = f"inventory_{player_id}"
        
        try:
            # Buscar objeto en el inventario del jugador
            inventory_objects = await self.memory_system.get_objects_in_location(player_inventory_id)
            target_object = None
            
            for obj in inventory_objects:
                if object_name in obj["name"].lower():
                    target_object = obj
                    break
            
            if not target_object:
                return {
                    "success": False,
                    "error": f"No tienes '{object_name}' en tu inventario",
                    "message": f"Inventario: {', '.join([obj['name'] for obj in inventory_objects])}"
                }
            
            # Mover objeto a la ubicación actual
            await self.memory_system.move_object(
                target_object["id"], 
                current_location,
                actor=f"player_{player_id}"
            )
            
            return {
                "success": True,
                "message": f"Dejas {target_object['name']} en el suelo",
                "new_state": {
                    "object_moved": True,
                    "object": target_object,
                    "from_location": player_inventory_id,
                    "to_location": current_location
                }
            }
            
        except Exception as e:
            logger.error(f"Error soltando objeto: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_look_around(self, player_id: str, current_location: str) -> Dict:
        """Maneja mirar alrededor"""
        try:
            location = await self.memory_system.get_location(current_location)
            objects = await self.memory_system.get_objects_in_location(current_location)
            other_players = self.session_manager.get_players_in_location(current_location)
            other_players = [p for p in other_players if p.id != player_id]
            
            description = location["description"]
            
            if objects:
                description += f"\nVes aquí: {', '.join([obj['name'] for obj in objects])}"
            
            if other_players:
                description += f"\nOtros jugadores aquí: {', '.join([p.username for p in other_players])}"
            
            return {
                "success": True,
                "message": description,
                "new_state": {
                    "location": location,
                    "objects": objects,
                    "other_players": [p.username for p in other_players]
                }
            }
            
        except Exception as e:
            logger.error(f"Error mirando alrededor: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_player_chat(self, player_id: str, action_data: Dict) -> Dict:
        """Maneja chat entre jugadores"""
        message = action_data.get("message", "")
        player = self.session_manager.players[player_id]
        
        # Broadcast del mensaje a otros jugadores en la misma ubicación
        chat_data = {
            "player_id": player_id,
            "username": player.username,
            "message": message,
            "location": player.current_location,
            "timestamp": datetime.now().isoformat()
        }
        
        # Enviar a jugadores en la misma ubicación
        players_in_location = self.session_manager.get_players_in_location(player.current_location)
        for other_player in players_in_location:
            if other_player.id != player_id and other_player.websocket_connection:
                try:
                    await other_player.websocket_connection.send_text(json.dumps({
                        "type": "player_chat",
                        "data": chat_data
                    }))
                except Exception as e:
                    logger.error(f"Error enviando chat a {other_player.username}: {e}")
        
        return {
            "success": True,
            "message": f"Dices: {message}",
            "new_state": {"chat_sent": True}
        }
    
    async def _handle_use_object(self, player_id: str, action_data: Dict) -> Dict:
        """Maneja usar un objeto"""
        # Implementación básica - puede expandirse
        return {
            "success": True,
            "message": "Funcionalidad 'usar objeto' en desarrollo",
            "new_state": {}
        }
    
    async def _apply_world_change(self, change: WorldChange):
        """Aplica un cambio al estado del mundo"""
        self.change_history.append(change)
        change.synchronized = True
        
        # Registrar en sistema de memoria si es necesario
        await self.memory_system._record_event(
            event_type="multiplayer_change",
            actor=f"player_{change.player_id}",
            action=change.change_type,
            context={
                "change_id": change.change_id,
                "target_id": change.target_id,
                "timestamp": change.timestamp.isoformat() if change.timestamp else None
            }
        )
    
    async def _broadcast_world_change(self, change: WorldChange, result: Dict):
        """Broadcast de un cambio del mundo a otros jugadores"""
        player = self.session_manager.players.get(change.player_id)
        if not player:
            return
        
        broadcast_data = {
            "change_id": change.change_id,
            "player_id": change.player_id,
            "player_name": player.username,
            "change_type": change.change_type,
            "result": result,
            "timestamp": change.timestamp.isoformat() if change.timestamp else None
        }
        
        # Enviar a todos los jugadores excepto quien hizo el cambio
        await self.session_manager.broadcast_world_event("world_change", broadcast_data)
    
    def get_world_state(self) -> Dict:
        """Obtiene el estado actual completo del mundo multi-jugador"""
        return {
            "players": {pid: player.to_dict() for pid, player in self.session_manager.players.items()},
            "pending_changes": len(self.pending_changes),
            "change_history_count": len(self.change_history),
            "session_stats": self.session_manager.get_session_stats(),
            "last_changes": [
                {
                    "change_id": change.change_id,
                    "player_id": change.player_id,
                    "change_type": change.change_type,
                    "timestamp": change.timestamp.isoformat() if change.timestamp else None
                }
                for change in self.change_history[-10:]  # Últimos 10 cambios
            ]
        }

# Función de utilidad para crear el sincronizador
def create_world_synchronizer(memory_system, session_manager):
    """Crea una instancia del sincronizador de mundo"""
    return WorldSynchronizer(memory_system, session_manager)
