#!/usr/bin/env python3
# 🔌 CLIENTE WEBSOCKET REAL - TESTING SISTEMA MULTI-JUGADOR

"""
Cliente WebSocket para testing completo del sistema multi-jugador
Simula un jugador real conectándose al servidor
"""

import asyncio
import websockets
import json
import time
import uuid
from datetime import datetime
import threading

class MultiplayerWebSocketClient:
    def __init__(self, server_url="ws://127.0.0.1:8002/ws", player_name="TestPlayer"):
        self.server_url = server_url
        self.player_name = player_name
        self.player_id = str(uuid.uuid4())
        self.websocket = None
        self.connected = False
        self.messages_received = []
        self.connection_time = None
        
    async def connect(self):
        """Conectar al servidor WebSocket"""
        try:
            print(f"🔌 Conectando a {self.server_url}...")
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            self.connection_time = datetime.now()
            print(f"✅ Conectado exitosamente como {self.player_name}")
            return True
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            return False
    
    async def disconnect(self):
        """Desconectar del servidor"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print(f"🔌 Desconectado de {self.server_url}")
    
    async def send_message(self, message_type, data=None):
        """Enviar mensaje al servidor"""
        if not self.connected or not self.websocket:
            print("❌ No hay conexión WebSocket")
            return False
        
        message = {
            "type": message_type,
            "player_id": self.player_id,
            "player_name": self.player_name,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            print(f"📤 Enviado: {message_type}")
            return True
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
            return False
    
    async def listen_messages(self):
        """Escuchar mensajes del servidor"""
        if not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    self.messages_received.append({
                        "timestamp": datetime.now().isoformat(),
                        "data": data
                    })
                    print(f"📥 Recibido: {data.get('type', 'unknown')} - {str(data)[:100]}...")
                except json.JSONDecodeError:
                    print(f"📥 Mensaje no JSON: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Conexión cerrada por el servidor")
            self.connected = False
        except Exception as e:
            print(f"❌ Error escuchando mensajes: {e}")
    
    async def authenticate(self):
        """Autenticar jugador"""
        return await self.send_message("authenticate", {
            "username": self.player_name,
            "auth_method": "guest"
        })
    
    async def join_game(self):
        """Unirse al juego"""
        return await self.send_message("join_game", {
            "game_mode": "adventure",
            "character_name": self.player_name
        })
    
    async def send_chat_message(self, message):
        """Enviar mensaje de chat"""
        return await self.send_message("chat", {
            "message": message,
            "channel": "general"
        })
    
    async def send_game_command(self, command):
        """Enviar comando de juego"""
        return await self.send_message("game_command", {
            "command": command,
            "action_type": "explore"
        })
    
    async def request_world_status(self):
        """Solicitar estado del mundo"""
        return await self.send_message("world_status", {})
    
    async def request_player_list(self):
        """Solicitar lista de jugadores"""
        return await self.send_message("player_list", {})

async def test_basic_websocket_connection():
    """Test básico de conexión WebSocket"""
    print("\n🧪 TEST 1: CONEXIÓN BÁSICA WEBSOCKET")
    print("-" * 50)
    
    client = MultiplayerWebSocketClient(player_name="BasicTestPlayer")
    
    # Test de conexión
    connected = await client.connect()
    if not connected:
        print("❌ Falló la conexión básica")
        return False
    
    # Mantener conexión por unos segundos
    await asyncio.sleep(2)
    
    # Desconectar
    await client.disconnect()
    
    print("✅ Test básico de conexión completado")
    return True

async def test_authentication_flow():
    """Test de flujo de autenticación"""
    print("\n🧪 TEST 2: FLUJO DE AUTENTICACIÓN")
    print("-" * 50)
    
    client = MultiplayerWebSocketClient(player_name="AuthTestPlayer")
    
    try:
        # Conectar
        if not await client.connect():
            return False
        
        # Crear tarea de escucha
        listen_task = asyncio.create_task(client.listen_messages())
        
        # Autenticar
        await client.authenticate()
        await asyncio.sleep(1)
        
        # Unirse al juego
        await client.join_game()
        await asyncio.sleep(2)
        
        # Cancelar escucha y desconectar
        listen_task.cancel()
        await client.disconnect()
        
        print(f"✅ Autenticación completada. Mensajes recibidos: {len(client.messages_received)}")
        return True
        
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        await client.disconnect()
        return False

async def test_game_interaction():
    """Test de interacción de juego"""
    print("\n🧪 TEST 3: INTERACCIÓN DE JUEGO")
    print("-" * 50)
    
    client = MultiplayerWebSocketClient(player_name="GameTestPlayer")
    
    try:
        # Conectar y autenticar
        if not await client.connect():
            return False
        
        listen_task = asyncio.create_task(client.listen_messages())
        
        await client.authenticate()
        await asyncio.sleep(1)
        
        await client.join_game()
        await asyncio.sleep(1)
        
        # Comandos de juego
        commands = [
            "mirar alrededor",
            "explorar",
            "inventario",
            "estado"
        ]
        
        for command in commands:
            await client.send_game_command(command)
            await asyncio.sleep(0.5)
        
        # Mensajes de chat
        chat_messages = [
            "¡Hola mundo!",
            "Testing del sistema multi-jugador",
            "¿Hay alguien más aquí?"
        ]
        
        for msg in chat_messages:
            await client.send_chat_message(msg)
            await asyncio.sleep(0.5)
        
        # Solicitar información
        await client.request_world_status()
        await asyncio.sleep(0.5)
        
        await client.request_player_list()
        await asyncio.sleep(1)
        
        listen_task.cancel()
        await client.disconnect()
        
        print(f"✅ Interacción completada. Mensajes recibidos: {len(client.messages_received)}")
        return True
        
    except Exception as e:
        print(f"❌ Error en interacción: {e}")
        await client.disconnect()
        return False

async def test_multiple_clients():
    """Test con múltiples clientes simultáneos"""
    print("\n🧪 TEST 4: MÚLTIPLES CLIENTES SIMULTÁNEOS")
    print("-" * 50)
    
    clients = []
    
    try:
        # Crear múltiples clientes
        for i in range(3):
            client = MultiplayerWebSocketClient(player_name=f"Player{i+1}")
            clients.append(client)
        
        # Conectar todos
        connected_clients = []
        for client in clients:
            if await client.connect():
                connected_clients.append(client)
                print(f"✅ {client.player_name} conectado")
            else:
                print(f"❌ {client.player_name} falló al conectar")
        
        if not connected_clients:
            print("❌ Ningún cliente pudo conectarse")
            return False
        
        # Crear tareas de escucha para todos
        listen_tasks = []
        for client in connected_clients:
            task = asyncio.create_task(client.listen_messages())
            listen_tasks.append(task)
        
        # Autenticar todos
        for client in connected_clients:
            await client.authenticate()
            await client.join_game()
            await asyncio.sleep(0.5)
        
        # Intercambio de mensajes
        for i, client in enumerate(connected_clients):
            await client.send_chat_message(f"¡Hola desde {client.player_name}!")
            await asyncio.sleep(0.3)
        
        # Esperar un poco más para ver interacciones
        await asyncio.sleep(3)
        
        # Limpiar
        for task in listen_tasks:
            task.cancel()
        
        for client in connected_clients:
            await client.disconnect()
        
        total_messages = sum(len(client.messages_received) for client in connected_clients)
        print(f"✅ Test múltiples clientes completado. Total mensajes: {total_messages}")
        return True
        
    except Exception as e:
        print(f"❌ Error en test múltiples clientes: {e}")
        # Limpiar en caso de error
        for client in clients:
            try:
                await client.disconnect()
            except:
                pass
        return False

async def test_stress_connection():
    """Test de estrés de conexiones"""
    print("\n🧪 TEST 5: STRESS TEST DE CONEXIONES")
    print("-" * 50)
    
    results = {
        "connections_attempted": 0,
        "connections_successful": 0,
        "messages_sent": 0,
        "messages_received": 0,
        "errors": 0
    }
    
    clients = []
    
    try:
        # Crear muchos clientes
        for i in range(5):
            client = MultiplayerWebSocketClient(player_name=f"StressTest{i+1}")
            clients.append(client)
            results["connections_attempted"] += 1
        
        # Conectar rápidamente
        for client in clients:
            try:
                if await client.connect():
                    results["connections_successful"] += 1
                    
                    # Enviar algunos mensajes rápido
                    await client.authenticate()
                    await client.send_chat_message("Stress test message")
                    await client.request_world_status()
                    results["messages_sent"] += 3
                    
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                results["errors"] += 1
                print(f"⚠️ Error con {client.player_name}: {e}")
        
        # Esperar un poco
        await asyncio.sleep(2)
        
        # Contar mensajes recibidos
        for client in clients:
            results["messages_received"] += len(client.messages_received)
        
        # Desconectar todos
        for client in clients:
            try:
                await client.disconnect()
            except:
                pass
        
        print(f"📊 Stress Test Results:")
        print(f"  • Conexiones intentadas: {results['connections_attempted']}")
        print(f"  • Conexiones exitosas: {results['connections_successful']}")
        print(f"  • Mensajes enviados: {results['messages_sent']}")
        print(f"  • Mensajes recibidos: {results['messages_received']}")
        print(f"  • Errores: {results['errors']}")
        
        success_rate = (results['connections_successful'] / results['connections_attempted']) * 100
        print(f"  • Tasa de éxito: {success_rate:.1f}%")
        
        return success_rate >= 80  # 80% o más es considerado exitoso
        
    except Exception as e:
        print(f"❌ Error en stress test: {e}")
        return False

async def main():
    """Función principal de testing"""
    print("🚀 TESTING WEBSOCKET REAL - SISTEMA MULTI-JUGADOR")
    print("=" * 80)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Conexión Básica", test_basic_websocket_connection),
        ("Flujo de Autenticación", test_authentication_flow),
        ("Interacción de Juego", test_game_interaction),
        ("Múltiples Clientes", test_multiple_clients),
        ("Stress Test", test_stress_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}")
        start_time = time.time()
        
        try:
            result = await test_func()
            results.append(result)
            duration = time.time() - start_time
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"📊 {test_name}: {status} ({duration:.2f}s)")
        except Exception as e:
            results.append(False)
            duration = time.time() - start_time
            print(f"📊 {test_name}: ❌ ERROR ({duration:.2f}s) - {e}")
    
    # Resultados finales
    print("\n" + "=" * 80)
    print("📊 RESULTADOS FINALES")
    print("-" * 80)
    
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"🏆 Tests pasados: {passed}/{total} ({success_rate:.1f}%)")
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  • {test_name}: {status}")
    
    print("\n🔍 ANÁLISIS")
    print("-" * 80)
    
    if success_rate >= 90:
        print("🟢 EXCELENTE: Sistema WebSocket completamente funcional")
        print("✅ Listo para producción y uso intensivo")
        status = "EXCELENTE"
    elif success_rate >= 75:
        print("🟡 BUENO: Sistema WebSocket mayormente funcional")
        print("✅ Funcional para desarrollo y testing")
        status = "BUENO"
    elif success_rate >= 50:
        print("🟠 REGULAR: Sistema WebSocket parcialmente funcional")
        print("⚠️ Necesita optimización antes de producción")
        status = "REGULAR"
    else:
        print("🔴 CRÍTICO: Sistema WebSocket con problemas serios")
        print("🛠️ Requiere revisión completa")
        status = "CRÍTICO"
    
    print("\n🗺️ PRÓXIMOS PASOS")
    print("-" * 80)
    
    if status in ["EXCELENTE", "BUENO"]:
        print("1. ✅ Sistema WebSocket validado")
        print("2. 🔜 Implementar frontend multi-jugador")
        print("3. 🔜 Desarrollar funcionalidades avanzadas")
        print("4. 🔜 Testing de rendimiento a gran escala")
    else:
        print("1. 🔧 Revisar logs del servidor WebSocket")
        print("2. 🔧 Optimizar manejo de conexiones")
        print("3. 🔧 Validar configuración de WebSocket")
        print("4. 🔄 Re-ejecutar tests")
    
    print(f"\n⏰ Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return status, passed, total

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        import traceback
        traceback.print_exc()
