# 🧪 TEST BÁSICO DE WEBSOCKET MULTI-JUGADOR

"""
Test básico para verificar la conexión WebSocket
"""

import asyncio
import json
import websockets
import aiohttp

async def test_basic_connection():
    """Test básico de conexión al servidor"""
    print("🔍 Testing conexión básica al servidor...")
    
    try:
        # Test HTTP básico
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:8002/") as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Servidor HTTP funcionando:", data.get("message", "OK"))
                else:
                    print("❌ Error en servidor HTTP:", response.status)
                    return False
    except Exception as e:
        print("❌ Error conectando al servidor HTTP:", e)
        return False
    
    try:
        # Test WebSocket básico
        uri = "ws://127.0.0.1:8002/ws/multiplayer"
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket conectado exitosamente")
            
            # Esperar mensaje inicial
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                print("✅ Mensaje inicial recibido:", data.get("type", "unknown"))
                return True
            except asyncio.TimeoutError:
                print("❌ Timeout esperando mensaje inicial")
                return False
                
    except Exception as e:
        print("❌ Error en conexión WebSocket:", e)
        return False

async def test_authentication():
    """Test de autenticación de jugador"""
    print("\n🔍 Testing autenticación de jugador...")
    
    try:
        uri = "ws://127.0.0.1:8002/ws/multiplayer"
        async with websockets.connect(uri) as websocket:
            
            # Esperar mensaje inicial
            initial_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            initial_data = json.loads(initial_response)
            print("✅ Conexión establecida:", initial_data.get("websocket_id", "unknown")[:8] + "...")
            
            # Enviar autenticación
            auth_message = {
                "type": "authenticate",
                "username": "TestPlayer",
                "role": "player"
            }
            
            await websocket.send(json.dumps(auth_message))
            print("📤 Mensaje de autenticación enviado")
            
            # Esperar respuesta de autenticación
            auth_response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            auth_data = json.loads(auth_response)
            
            if auth_data.get("response", {}).get("success"):
                player_id = auth_data["response"]["player_id"]
                print("✅ Autenticación exitosa, Player ID:", player_id[:8] + "...")
                return True
            else:
                print("❌ Autenticación falló:", auth_data.get("response", {}).get("error", "Unknown error"))
                return False
                
    except Exception as e:
        print("❌ Error en test de autenticación:", e)
        return False

async def test_game_command():
    """Test de comando del juego"""
    print("\n🔍 Testing comando del juego...")
    
    try:
        uri = "ws://127.0.0.1:8002/ws/multiplayer"
        async with websockets.connect(uri) as websocket:
            
            # Conexión y autenticación
            await websocket.recv()  # Mensaje inicial
            
            auth_message = {"type": "authenticate", "username": "CommandTester", "role": "player"}
            await websocket.send(json.dumps(auth_message))
            await websocket.recv()  # Respuesta de autenticación
            
            # Enviar comando del juego
            game_command = {
                "type": "game_command",
                "command": "mirar"
            }
            
            await websocket.send(json.dumps(game_command))
            print("📤 Comando 'mirar' enviado")
            
            # Esperar respuesta
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            response_data = json.loads(response)
            
            if response_data.get("response", {}).get("success"):
                print("✅ Comando ejecutado exitosamente")
                result = response_data["response"].get("result", "")
                if result:
                    print("📝 Resultado:", result[:100] + "..." if len(result) > 100 else result)
                return True
            else:
                print("❌ Comando falló:", response_data.get("response", {}).get("error", "Unknown error"))
                return False
                
    except Exception as e:
        print("❌ Error en test de comando:", e)
        return False

async def test_api_endpoints():
    """Test de endpoints de la API"""
    print("\n🔍 Testing endpoints de la API...")
    
    headers = {"Authorization": "Bearer admin-token"}
    
    endpoints = [
        ("/api/health", "Health Check"),
        ("/api/metrics", "Métricas del sistema"),
        ("/api/multiplayer/status", "Estado multi-jugador")
    ]
    
    success_count = 0
    
    try:
        async with aiohttp.ClientSession() as session:
            for endpoint, description in endpoints:
                try:
                    async with session.get(f"http://127.0.0.1:8002{endpoint}", headers=headers) as response:
                        if response.status == 200:
                            print(f"✅ {description}: OK")
                            success_count += 1
                        else:
                            print(f"❌ {description}: Error {response.status}")
                except Exception as e:
                    print(f"❌ {description}: Exception {e}")
    
        return success_count == len(endpoints)
        
    except Exception as e:
        print("❌ Error general en test de API:", e)
        return False

async def main():
    """Función principal de testing"""
    print("🧪 SISTEMA DE TESTING BÁSICO MULTI-JUGADOR")
    print("=" * 50)
    print("Servidor: http://127.0.0.1:8002")
    print("WebSocket: ws://127.0.0.1:8002/ws/multiplayer")
    print()
    
    tests = [
        ("Conexión básica", test_basic_connection),
        ("Autenticación", test_authentication), 
        ("Comando del juego", test_game_command),
        ("Endpoints API", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Tests pasados: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 ¡TODOS LOS TESTS BÁSICOS PASARON!")
    else:
        print("⚠️ Algunos tests necesitan atención")

if __name__ == "__main__":
    asyncio.run(main())
