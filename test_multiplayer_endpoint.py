#!/usr/bin/env python3
# 🎮 TEST ESPECÍFICO PARA ENDPOINT MULTIPLAYER

"""
Test completo del endpoint /ws/multiplayer con todas las funcionalidades
"""

import asyncio
import websockets
import json
import logging
import time
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiPlayerWebSocketTester:
    """Tester completo para WebSocket multi-jugador"""
    
    def __init__(self, base_url="ws://localhost:8000"):
        self.base_url = base_url
        self.connections = {}
        self.test_results = []
    
    async def test_basic_connection(self):
        """Test 1: Conexión básica al endpoint multiplayer"""
        print("🧪 TEST 1: CONEXIÓN BÁSICA MULTIPLAYER")
        print("-" * 50)
        
        try:
            uri = f"{self.base_url}/ws/multiplayer"
            async with websockets.connect(uri, timeout=10) as websocket:
                print(f"✅ Conectado a {uri}")
                
                # Esperar mensaje inicial
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5)
                    data = json.loads(message)
                    print(f"📥 Mensaje inicial recibido:")
                    print(f"   Tipo: {data.get('type', 'N/A')}")
                    print(f"   Status: {data.get('status', 'N/A')}")
                    print(f"   Message: {data.get('message', 'N/A')}")
                    
                    self.test_results.append(("Conexión Multiplayer", True))
                    return True
                    
                except asyncio.TimeoutError:
                    print(f"⏰ No se recibió mensaje inicial")
                    self.test_results.append(("Conexión Multiplayer", False))
                    return False
                    
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            self.test_results.append(("Conexión Multiplayer", False))
            return False
    
    async def test_authentication_flow(self):
        """Test 2: Flujo de autenticación de jugador"""
        print(f"\n🧪 TEST 2: AUTENTICACIÓN DE JUGADOR")
        print("-" * 50)
        
        try:
            uri = f"{self.base_url}/ws/multiplayer"
            async with websockets.connect(uri, timeout=10) as websocket:
                print(f"✅ Conectado para autenticación")
                
                # Enviar autenticación
                auth_message = {
                    "type": "authenticate",
                    "player_name": "TestPlayer1",
                    "session_id": f"test-session-{int(time.time())}"
                }
                await websocket.send(json.dumps(auth_message))
                print(f"📤 Enviado: {auth_message}")
                
                # Esperar respuesta de autenticación
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(response)
                    print(f"📥 Respuesta de auth:")
                    print(f"   Tipo: {data.get('type', 'N/A')}")
                    print(f"   Success: {data.get('success', 'N/A')}")
                    print(f"   Player ID: {data.get('player_id', 'N/A')}")
                    print(f"   Session ID: {data.get('session_id', 'N/A')}")
                    
                    success = data.get('success', False)
                    self.test_results.append(("Autenticación", success))
                    return success
                    
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout esperando respuesta de auth")
                    self.test_results.append(("Autenticación", False))
                    return False
                    
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            self.test_results.append(("Autenticación", False))
            return False
    
    async def test_game_commands(self):
        """Test 3: Comandos de juego"""
        print(f"\n🧪 TEST 3: COMANDOS DE JUEGO")
        print("-" * 50)
        
        try:
            uri = f"{self.base_url}/ws/multiplayer"
            async with websockets.connect(uri, timeout=10) as websocket:
                
                # Autenticarse primero
                auth_message = {
                    "type": "authenticate",
                    "player_name": "CommandTester",
                    "session_id": f"cmd-test-{int(time.time())}"
                }
                await websocket.send(json.dumps(auth_message))
                
                # Esperar respuesta de auth
                await asyncio.wait_for(websocket.recv(), timeout=5)
                
                # Test comando: look
                look_command = {
                    "type": "game_command",
                    "command": "look",
                    "args": []
                }
                await websocket.send(json.dumps(look_command))
                print(f"📤 Comando enviado: look")
                
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(response)
                    print(f"📥 Respuesta comando:")
                    print(f"   Tipo: {data.get('type', 'N/A')}")
                    print(f"   Result: {data.get('result', 'N/A')[:100]}...")
                    
                    self.test_results.append(("Comandos de Juego", True))
                    return True
                    
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout esperando respuesta de comando")
                    self.test_results.append(("Comandos de Juego", False))
                    return False
                    
        except Exception as e:
            print(f"❌ Error en comandos: {e}")
            self.test_results.append(("Comandos de Juego", False))
            return False
    
    async def test_multiple_players(self):
        """Test 4: Múltiples jugadores simultáneos"""
        print(f"\n🧪 TEST 4: MÚLTIPLES JUGADORES")
        print("-" * 50)
        
        players = []
        try:
            # Conectar 3 jugadores
            for i in range(3):
                uri = f"{self.base_url}/ws/multiplayer"
                websocket = await websockets.connect(uri, timeout=10)
                
                # Autenticar cada jugador
                auth_message = {
                    "type": "authenticate",
                    "player_name": f"Player{i+1}",
                    "session_id": f"multi-test-{i+1}-{int(time.time())}"
                }
                await websocket.send(json.dumps(auth_message))
                
                # Esperar respuesta
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                data = json.loads(response)
                
                if data.get('success'):
                    players.append(websocket)
                    print(f"✅ Jugador {i+1} conectado: {data.get('player_id')}")
                else:
                    await websocket.close()
                    print(f"❌ Jugador {i+1} falló autenticación")
            
            print(f"📊 Jugadores conectados: {len(players)}")
            
            # Test comunicación entre jugadores
            if len(players) >= 2:
                # Player 1 envía mensaje
                chat_message = {
                    "type": "chat",
                    "message": "Hola a todos desde Player1!"
                }
                await players[0].send(json.dumps(chat_message))
                print(f"📤 Player1 envió chat: {chat_message['message']}")
                
                # Verificar que otros jugadores reciban el mensaje
                received_count = 0
                for i, player in enumerate(players[1:], 2):
                    try:
                        response = await asyncio.wait_for(player.recv(), timeout=3)
                        data = json.loads(response)
                        if data.get('type') == 'chat':
                            received_count += 1
                            print(f"📥 Player{i} recibió chat")
                    except asyncio.TimeoutError:
                        print(f"⏰ Player{i} no recibió chat")
                
                success = received_count > 0
                self.test_results.append(("Múltiples Jugadores", success))
                print(f"📊 Mensajes recibidos: {received_count}/{len(players)-1}")
            
            # Cerrar conexiones
            for player in players:
                await player.close()
            
            return len(players) >= 2
            
        except Exception as e:
            print(f"❌ Error en test multi-jugador: {e}")
            # Cerrar conexiones abiertas
            for player in players:
                try:
                    await player.close()
                except:
                    pass
            self.test_results.append(("Múltiples Jugadores", False))
            return False
    
    async def test_real_time_sync(self):
        """Test 5: Sincronización en tiempo real"""
        print(f"\n🧪 TEST 5: SINCRONIZACIÓN TIEMPO REAL")
        print("-" * 50)
        
        try:
            uri = f"{self.base_url}/ws/multiplayer"
            async with websockets.connect(uri, timeout=10) as websocket:
                
                # Autenticarse
                auth_message = {
                    "type": "authenticate",
                    "player_name": "SyncTester",
                    "session_id": f"sync-test-{int(time.time())}"
                }
                await websocket.send(json.dumps(auth_message))
                await asyncio.wait_for(websocket.recv(), timeout=5)
                
                # Ejecutar acción que afecte el mundo
                action_message = {
                    "type": "game_command",
                    "command": "inventory",
                    "args": []
                }
                await websocket.send(json.dumps(action_message))
                print(f"📤 Comando sincronización enviado")
                
                # Escuchar múltiples mensajes (sincronización)
                sync_messages = 0
                for i in range(3):
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=3)
                        data = json.loads(response)
                        print(f"📥 Mensaje sync {i+1}: {data.get('type', 'N/A')}")
                        sync_messages += 1
                    except asyncio.TimeoutError:
                        break
                
                success = sync_messages > 0
                self.test_results.append(("Sincronización", success))
                print(f"📊 Mensajes de sincronización: {sync_messages}")
                return success
                
        except Exception as e:
            print(f"❌ Error en sincronización: {e}")
            self.test_results.append(("Sincronización", False))
            return False
    
    async def run_all_tests(self):
        """Ejecutar todos los tests"""
        print("🚀 INICIANDO TESTS COMPLETOS DEL ENDPOINT MULTIPLAYER")
        print("=" * 70)
        print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        tests = [
            ("Conexión Básica", self.test_basic_connection),
            ("Autenticación", self.test_authentication_flow),
            ("Comandos de Juego", self.test_game_commands),
            ("Múltiples Jugadores", self.test_multiple_players),
            ("Sincronización", self.test_real_time_sync),
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Ejecutando: {test_name}")
            start_time = time.time()
            
            try:
                result = await test_func()
                duration = time.time() - start_time
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"📊 {test_name}: {status} ({duration:.2f}s)")
            except Exception as e:
                duration = time.time() - start_time
                print(f"📊 {test_name}: ❌ ERROR ({duration:.2f}s) - {e}")
                self.test_results.append((test_name, False))
        
        # Mostrar resultados finales
        self.show_results()
    
    def show_results(self):
        """Mostrar resultados finales"""
        print("\n" + "=" * 70)
        print("📊 RESULTADOS FINALES - ENDPOINT MULTIPLAYER")
        print("-" * 70)
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        print(f"🏆 Tests pasados: {passed}/{total} ({passed/total*100:.1f}%)")
        
        for test_name, result in self.test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  • {test_name}: {status}")
        
        # Diagnóstico
        print(f"\n🔍 DIAGNÓSTICO FINAL")
        print("-" * 70)
        
        if passed == total:
            print("🟢 TODOS LOS TESTS PASARON")
            print("🎉 El endpoint /ws/multiplayer está completamente funcional")
            print("✅ Listo para producción")
        elif passed >= total * 0.8:
            print("🟡 MAYORÍA DE TESTS PASARON")
            print("👍 El endpoint funciona en general")
            print("🔧 Algunos ajustes menores requeridos")
        else:
            print("🔴 MÚLTIPLES PROBLEMAS DETECTADOS")
            print("🛠️ Requiere revisión y correcciones")
        
        print(f"\n⏰ Completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

async def main():
    """Función principal"""
    tester = MultiPlayerWebSocketTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n⚠️ Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n❌ Error en main: {e}")
        import traceback
        traceback.print_exc()
