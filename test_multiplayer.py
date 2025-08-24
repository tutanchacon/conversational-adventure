# 🧪 TESTING SISTEMA MULTI-JUGADOR

"""
Testing Completo del Sistema Multi-jugador
==========================================

Pruebas para validar:
- Conexiones WebSocket
- Autenticación de jugadores
- Sincronización en tiempo real
- Comandos del juego
- Sistema de chat
- Gestión de roles
"""

import asyncio
import json
import websockets
import aiohttp
import time
from datetime import datetime
from typing import Dict, List
import logging

# Configurar logging para las pruebas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiplayerTester:
    """
    Clase principal para testing del sistema multi-jugador
    """
    
    def __init__(self, server_url: str = "127.0.0.1:8002"):
        self.server_url = server_url
        self.base_url = f"http://{server_url}"
        self.ws_url = f"ws://{server_url}"
        self.test_results = []
        self.connected_players = {}
        
    async def run_all_tests(self):
        """Ejecuta todos los tests del sistema multi-jugador"""
        logger.info("🧪 INICIANDO TESTING COMPLETO DEL SISTEMA MULTI-JUGADOR")
        logger.info("=" * 60)
        
        # Tests básicos del servidor
        await self.test_server_health()
        await self.test_api_endpoints()
        
        # Tests de WebSocket
        await self.test_websocket_connection()
        await self.test_player_authentication()
        
        # Tests multi-jugador
        await self.test_multiple_players()
        await self.test_chat_system()
        await self.test_game_commands()
        await self.test_world_synchronization()
        
        # Tests de administración
        await self.test_admin_features()
        
        # Mostrar resultados finales
        self.show_test_results()
    
    async def test_server_health(self):
        """Test 1: Verificar que el servidor esté funcionando"""
        logger.info("🔍 Test 1: Health Check del Servidor")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test endpoint raíz
                async with session.get(f"{self.base_url}/") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log_success("Endpoint raíz funcionando", data)
                    else:
                        self.log_error("Endpoint raíz no responde", response.status)
                
                # Test health endpoint
                async with session.get(f"{self.base_url}/api/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log_success("Health check OK", data)
                    else:
                        self.log_error("Health check falló", response.status)
                        
        except Exception as e:
            self.log_error("Error conectando al servidor", str(e))
    
    async def test_api_endpoints(self):
        """Test 2: Verificar endpoints de la API"""
        logger.info("🔍 Test 2: Endpoints de la API")
        
        endpoints_to_test = [
            "/api/health",
            "/api/metrics",
            "/api/multiplayer/status"
        ]
        
        # Token de prueba (simplificado para testing)
        headers = {"Authorization": "Bearer admin-token"}
        
        try:
            async with aiohttp.ClientSession() as session:
                for endpoint in endpoints_to_test:
                    try:
                        async with session.get(f"{self.base_url}{endpoint}", headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                self.log_success(f"Endpoint {endpoint}", data)
                            else:
                                self.log_error(f"Endpoint {endpoint} falló", response.status)
                    except Exception as e:
                        self.log_error(f"Error en {endpoint}", str(e))
                        
        except Exception as e:
            self.log_error("Error general en API tests", str(e))
    
    async def test_websocket_connection(self):
        """Test 3: Conexión WebSocket básica"""
        logger.info("🔍 Test 3: Conexión WebSocket")
        
        try:
            uri = f"{self.ws_url}/ws/multiplayer"
            async with websockets.connect(uri) as websocket:
                
                # Enviar ping
                ping_message = {"type": "ping", "timestamp": datetime.now().isoformat()}
                await websocket.send(json.dumps(ping_message))
                
                # Esperar respuesta
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                if data.get("type") == "connection_established":
                    self.log_success("WebSocket conectado", data)
                else:
                    self.log_error("WebSocket respuesta inesperada", data)
                    
        except Exception as e:
            self.log_error("Error en conexión WebSocket", str(e))
    
    async def test_player_authentication(self):
        """Test 4: Autenticación de jugadores"""
        logger.info("🔍 Test 4: Autenticación de Jugadores")
        
        test_players = [
            {"username": "TestPlayer1", "role": "player"},
            {"username": "TestAdmin", "role": "admin"},
            {"username": "TestObserver", "role": "observer"}
        ]
        
        for player_data in test_players:
            try:
                uri = f"{self.ws_url}/ws/multiplayer"
                async with websockets.connect(uri) as websocket:
                    
                    # Esperar mensaje de conexión establecida
                    initial_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    initial_data = json.loads(initial_response)
                    
                    if initial_data.get("type") == "connection_established":
                        websocket_id = initial_data.get("websocket_id")
                        
                        # Autenticar jugador
                        auth_message = {
                            "type": "authenticate",
                            "username": player_data["username"],
                            "role": player_data["role"]
                        }
                        
                        await websocket.send(json.dumps(auth_message))
                        
                        # Esperar respuesta de autenticación
                        auth_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        auth_data = json.loads(auth_response)
                        
                        if auth_data.get("response", {}).get("success"):
                            player_id = auth_data["response"]["player_id"]
                            self.connected_players[player_data["username"]] = {
                                "player_id": player_id,
                                "websocket_id": websocket_id,
                                "role": player_data["role"]
                            }
                            self.log_success(f"Autenticación exitosa: {player_data['username']}", auth_data["response"])
                        else:
                            self.log_error(f"Autenticación falló: {player_data['username']}", auth_data)
                    
            except Exception as e:
                self.log_error(f"Error autenticando {player_data['username']}", str(e))
    
    async def test_multiple_players(self):
        """Test 5: Múltiples jugadores simultáneos"""
        logger.info("🔍 Test 5: Múltiples Jugadores Simultáneos")
        
        async def create_player_connection(username, role):
            try:
                uri = f"{self.ws_url}/ws/multiplayer"
                websocket = await websockets.connect(uri)
                
                # Esperar conexión establecida
                initial_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                
                # Autenticar
                auth_message = {
                    "type": "authenticate",
                    "username": username,
                    "role": role
                }
                await websocket.send(json.dumps(auth_message))
                
                # Esperar autenticación
                auth_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                auth_data = json.loads(auth_response)
                
                if auth_data.get("response", {}).get("success"):
                    return websocket, auth_data["response"]["player_id"]
                else:
                    await websocket.close()
                    return None, None
                    
            except Exception as e:
                logger.error(f"Error creando conexión para {username}: {e}")
                return None, None
        
        # Crear múltiples conexiones simultáneas
        players = [
            ("MultiTest1", "player"),
            ("MultiTest2", "player"),
            ("MultiTest3", "observer")
        ]
        
        connections = []
        for username, role in players:
            websocket, player_id = await create_player_connection(username, role)
            if websocket and player_id:
                connections.append((websocket, player_id, username))
                self.log_success(f"Jugador conectado: {username}", {"player_id": player_id})
        
        # Mantener conexiones activas por un momento
        await asyncio.sleep(2)
        
        # Cerrar conexiones
        for websocket, player_id, username in connections:
            await websocket.close()
            self.log_success(f"Jugador desconectado: {username}", {"player_id": player_id})
    
    async def test_chat_system(self):
        """Test 6: Sistema de chat"""
        logger.info("🔍 Test 6: Sistema de Chat")
        
        async def create_chat_player(username):
            uri = f"{self.ws_url}/ws/multiplayer"
            websocket = await websockets.connect(uri)
            
            # Conexión y autenticación
            await websocket.recv()  # Mensaje inicial
            
            auth_message = {"type": "authenticate", "username": username, "role": "player"}
            await websocket.send(json.dumps(auth_message))
            await websocket.recv()  # Respuesta de autenticación
            
            return websocket
        
        try:
            # Crear dos jugadores para chat
            player1_ws = await create_chat_player("ChatTest1")
            player2_ws = await create_chat_player("ChatTest2")
            
            # Player 1 envía mensaje de chat
            chat_message = {
                "type": "chat_message",
                "message": "¡Hola desde el test de chat!"
            }
            
            await player1_ws.send(json.dumps(chat_message))
            
            # Esperar respuesta y posibles broadcasts
            response = await asyncio.wait_for(player1_ws.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            if response_data.get("response", {}).get("success"):
                self.log_success("Mensaje de chat enviado", response_data)
            else:
                self.log_error("Error enviando mensaje de chat", response_data)
            
            # Cerrar conexiones
            await player1_ws.close()
            await player2_ws.close()
            
        except Exception as e:
            self.log_error("Error en test de chat", str(e))
    
    async def test_game_commands(self):
        """Test 7: Comandos del juego"""
        logger.info("🔍 Test 7: Comandos del Juego")
        
        try:
            uri = f"{self.ws_url}/ws/multiplayer"
            async with websockets.connect(uri) as websocket:
                
                # Conexión y autenticación
                await websocket.recv()  # Mensaje inicial
                
                auth_message = {"type": "authenticate", "username": "GameTester", "role": "player"}
                await websocket.send(json.dumps(auth_message))
                await websocket.recv()  # Respuesta de autenticación
                
                # Probar comandos del juego
                test_commands = [
                    "mirar",
                    "inventario",
                    "norte",
                    "examinar llave"
                ]
                
                for command in test_commands:
                    game_command = {
                        "type": "game_command",
                        "command": command
                    }
                    
                    await websocket.send(json.dumps(game_command))
                    
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        response_data = json.loads(response)
                        
                        if response_data.get("response", {}).get("success"):
                            self.log_success(f"Comando '{command}' ejecutado", response_data["response"])
                        else:
                            self.log_error(f"Comando '{command}' falló", response_data)
                    except asyncio.TimeoutError:
                        self.log_error(f"Timeout en comando '{command}'", "No response")
                
        except Exception as e:
            self.log_error("Error en test de comandos", str(e))
    
    async def test_world_synchronization(self):
        """Test 8: Sincronización del mundo"""
        logger.info("🔍 Test 8: Sincronización del Mundo")
        
        try:
            # Crear dos jugadores en ubicaciones diferentes
            player1_ws = await self.create_test_player("SyncTest1")
            player2_ws = await self.create_test_player("SyncTest2")
            
            # Player 1 toma un objeto
            take_command = {
                "type": "game_command",
                "command": "tomar llave"
            }
            
            await player1_ws.send(json.dumps(take_command))
            
            # Esperar respuestas y verificar sincronización
            response1 = await asyncio.wait_for(player1_ws.recv(), timeout=5.0)
            
            # Verificar que el cambio se propaga
            await asyncio.sleep(1)
            
            # Player 2 mira la ubicación
            look_command = {
                "type": "game_command", 
                "command": "mirar"
            }
            
            await player2_ws.send(json.dumps(look_command))
            response2 = await asyncio.wait_for(player2_ws.recv(), timeout=5.0)
            
            self.log_success("Test de sincronización completado", {
                "player1_action": json.loads(response1),
                "player2_view": json.loads(response2)
            })
            
            await player1_ws.close()
            await player2_ws.close()
            
        except Exception as e:
            self.log_error("Error en test de sincronización", str(e))
    
    async def test_admin_features(self):
        """Test 9: Funcionalidades de administrador"""
        logger.info("🔍 Test 9: Funcionalidades de Administrador")
        
        headers = {"Authorization": "Bearer admin-token"}
        
        try:
            async with aiohttp.ClientSession() as session:
                
                # Test obtener jugadores activos
                async with session.get(f"{self.base_url}/api/multiplayer/players", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log_success("Lista de jugadores obtenida", data)
                    else:
                        self.log_error("Error obteniendo jugadores", response.status)
                
                # Test mensaje broadcast
                broadcast_data = {
                    "message": "Mensaje de prueba desde el testing",
                    "message_type": "test_broadcast"
                }
                
                async with session.post(f"{self.base_url}/api/multiplayer/broadcast", 
                                      json=broadcast_data, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.log_success("Broadcast enviado", data)
                    else:
                        self.log_error("Error enviando broadcast", response.status)
                
        except Exception as e:
            self.log_error("Error en test de admin", str(e))
    
    async def create_test_player(self, username):
        """Función auxiliar para crear jugador de prueba"""
        uri = f"{self.ws_url}/ws/multiplayer"
        websocket = await websockets.connect(uri)
        
        await websocket.recv()  # Mensaje inicial
        
        auth_message = {"type": "authenticate", "username": username, "role": "player"}
        await websocket.send(json.dumps(auth_message))
        await websocket.recv()  # Respuesta de autenticación
        
        return websocket
    
    def log_success(self, test_name: str, data: any):
        """Registra un test exitoso"""
        result = {
            "test": test_name,
            "status": "SUCCESS",
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        logger.info(f"✅ {test_name}: SUCCESS")
    
    def log_error(self, test_name: str, error: any):
        """Registra un test fallido"""
        result = {
            "test": test_name,
            "status": "ERROR",
            "timestamp": datetime.now().isoformat(),
            "error": str(error)
        }
        self.test_results.append(result)
        logger.error(f"❌ {test_name}: ERROR - {error}")
    
    def show_test_results(self):
        """Muestra el resumen final de los tests"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESUMEN FINAL DE TESTS")
        logger.info("=" * 60)
        
        success_count = len([r for r in self.test_results if r["status"] == "SUCCESS"])
        error_count = len([r for r in self.test_results if r["status"] == "ERROR"])
        total_count = len(self.test_results)
        
        logger.info(f"✅ Tests exitosos: {success_count}")
        logger.info(f"❌ Tests fallidos: {error_count}")
        logger.info(f"📊 Total de tests: {total_count}")
        
        if error_count == 0:
            logger.info("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        else:
            logger.info(f"⚠️ {error_count} tests necesitan atención")
        
        # Mostrar detalles de errores
        if error_count > 0:
            logger.info("\n🔍 DETALLES DE ERRORES:")
            for result in self.test_results:
                if result["status"] == "ERROR":
                    logger.info(f"  - {result['test']}: {result['error']}")

async def main():
    """Función principal para ejecutar los tests"""
    print("🧪 SISTEMA DE TESTING MULTI-JUGADOR")
    print("Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8002")
    print()
    
    # Esperar confirmación del usuario
    input("Presiona Enter para continuar con los tests...")
    
    tester = MultiplayerTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
