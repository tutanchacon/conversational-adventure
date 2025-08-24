#!/usr/bin/env python3
# 🧪 TEST SIMPLIFICADO CON AIOHTTP - SISTEMA MULTI-JUGADOR

import asyncio
import aiohttp
import json

async def test_http_endpoints():
    """Test de todos los endpoints HTTP del servidor"""
    print("🔍 Testing endpoints HTTP del servidor multi-jugador...")
    
    endpoints = [
        ("GET", "/", "Endpoint principal"),
        ("GET", "/health", "Endpoint de salud"),
        ("GET", "/api/info", "Información de API"),
        ("GET", "/api/multiplayer/world/status", "Estado del mundo multi-jugador"),
        ("GET", "/api/multiplayer/players", "Lista de jugadores"),
        ("GET", "/api/multiplayer/sessions", "Sesiones activas")
    ]
    
    async with aiohttp.ClientSession() as session:
        results = []
        
        for method, endpoint, description in endpoints:
            try:
                url = f"http://127.0.0.1:8002{endpoint}"
                print(f"  🔗 Testing {description}: {endpoint}")
                
                async with session.request(method, url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"    ✅ OK ({response.status}): {json.dumps(data, indent=2)[:100]}...")
                        results.append(True)
                    else:
                        print(f"    ❌ Error {response.status}")
                        results.append(False)
                        
            except Exception as e:
                print(f"    ❌ Excepción: {e}")
                results.append(False)
        
        return results

async def test_multiplayer_authentication():
    """Test básico de autenticación multi-jugador"""
    print("🔍 Testing autenticación multi-jugador...")
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test de inicio de sesión
            login_data = {
                "username": "test_player",
                "password": "test_password"
            }
            
            url = "http://127.0.0.1:8002/api/multiplayer/auth/login"
            async with session.post(url, json=login_data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"  ✅ Login OK: {data}")
                    return True
                else:
                    print(f"  ❌ Login Error {response.status}")
                    return False
                    
        except Exception as e:
            print(f"  ❌ Excepción en autenticación: {e}")
            return False

async def test_multiplayer_session_creation():
    """Test de creación de sesión de juego"""
    print("🔍 Testing creación de sesión...")
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test de creación de sesión
            session_data = {
                "player_name": "TestPlayer",
                "session_type": "adventure"
            }
            
            url = "http://127.0.0.1:8002/api/multiplayer/sessions/create"
            async with session.post(url, json=session_data) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    print(f"  ✅ Sesión creada: {data}")
                    return True
                else:
                    print(f"  ❌ Error creando sesión {response.status}")
                    return False
                    
        except Exception as e:
            print(f"  ❌ Excepción en creación de sesión: {e}")
            return False

async def main():
    """Función principal de testing"""
    print("🚀 TESTING SISTEMA MULTI-JUGADOR v2.0")
    print("=" * 60)
    
    # Test 1: Endpoints HTTP
    print("\n📡 TEST 1: ENDPOINTS HTTP")
    print("-" * 40)
    endpoint_results = await test_http_endpoints()
    
    # Test 2: Autenticación
    print("\n🔐 TEST 2: AUTENTICACIÓN")
    print("-" * 40)
    auth_result = await test_multiplayer_authentication()
    
    # Test 3: Creación de sesión
    print("\n🎮 TEST 3: CREACIÓN DE SESIÓN")
    print("-" * 40)
    session_result = await test_multiplayer_session_creation()
    
    # Resultados finales
    print("\n" + "=" * 60)
    print("📊 RESULTADOS FINALES")
    print("-" * 60)
    
    total_endpoints = len(endpoint_results)
    passed_endpoints = sum(endpoint_results)
    
    print(f"📡 Endpoints HTTP: {passed_endpoints}/{total_endpoints}")
    print(f"🔐 Autenticación: {'✅ PASS' if auth_result else '❌ FAIL'}")
    print(f"🎮 Creación sesión: {'✅ PASS' if session_result else '❌ FAIL'}")
    
    total_tests = total_endpoints + 2
    passed_tests = passed_endpoints + (1 if auth_result else 0) + (1 if session_result else 0)
    
    print(f"\n🏆 TOTAL: {passed_tests}/{total_tests} tests pasaron")
    
    if passed_tests == total_tests:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Sistema multi-jugador listo para WebSocket testing")
    elif passed_tests >= total_tests * 0.7:
        print("⚠️ La mayoría de tests pasaron, sistema funcional")
        print("💡 Revisar endpoints que fallaron")
    else:
        print("❌ Muchos tests fallaron")
        print("🔧 Revisar configuración del servidor")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
