# 🎮 SISTEMA MULTI-JUGADOR ADVENTURE GAME

"""
Módulo Multi-jugador para Adventure Game
======================================

Sistema completo de multi-jugador en tiempo real con:

🔌 WebSocket para comunicación en tiempo real
👥 Gestión de sesiones de jugadores
🌍 Sincronización del mundo del juego
🎯 Roles de jugador (Admin, Jugador, Observador)
💬 Sistema de chat integrado
📊 Métricas y estadísticas de servidor

Componentes principales:
- session_manager.py: Gestión de jugadores y sesiones
- world_synchronizer.py: Sincronización del estado del mundo
- multiplayer_game.py: Orquestador principal del juego multi-jugador
- websocket_handler.py: Manejo de conexiones WebSocket

Uso:
    from multiplayer import get_multiplayer_game
    
    game = get_multiplayer_game()
    await game.initialize(memory_system)
"""

from .session_manager import PlayerRole, MultiPlayerSessionManager
from .world_synchronizer import WorldSynchronizer
from .multiplayer_game import MultiPlayerGameManager, get_multiplayer_game
from .websocket_handler import websocket_manager, websocket_endpoint

__version__ = "1.0.0"
__author__ = "Adventure Game Team"

__all__ = [
    "PlayerRole",
    "MultiPlayerSessionManager", 
    "WorldSynchronizer",
    "MultiPlayerGameManager",
    "get_multiplayer_game",
    "websocket_manager",
    "websocket_endpoint"
]
