#!/usr/bin/env python3
# 🧪 TEST BÁSICO CON URLLIB - SISTEMA MULTI-JUGADOR
# Solo usa bibliotecas estándar de Python

import urllib.request
import urllib.parse
import json
import time

def test_endpoint(endpoint, description):
    """Test individual de un endpoint"""
    url = f"http://127.0.0.1:8002{endpoint}"
    print(f"  🔗 Testing {description}: {endpoint}")
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = response.read().decode('utf-8')
                try:
                    json_data = json.loads(data)
                    print(f"    ✅ OK ({response.status}): {str(json_data)[:100]}...")
                    return True
                except json.JSONDecodeError:
                    print(f"    ✅ OK ({response.status}): {data[:100]}...")
                    return True
            else:
                print(f"    ❌ Error {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"    ❌ HTTP Error {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"    ❌ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"    ❌ Excepción: {e}")
        return False

def test_post_endpoint(endpoint, data, description):
    """Test de endpoint POST"""
    url = f"http://127.0.0.1:8002{endpoint}"
    print(f"  🔗 Testing {description}: {endpoint}")
    
    try:
        # Preparar datos
        json_data = json.dumps(data).encode('utf-8')
        
        # Crear request
        req = urllib.request.Request(
            url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status in [200, 201]:
                response_data = response.read().decode('utf-8')
                try:
                    json_response = json.loads(response_data)
                    print(f"    ✅ OK ({response.status}): {str(json_response)[:100]}...")
                    return True
                except json.JSONDecodeError:
                    print(f"    ✅ OK ({response.status}): {response_data[:100]}...")
                    return True
            else:
                print(f"    ❌ Error {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"    ❌ HTTP Error {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"    ❌ URL Error: {e.reason}")
        return False
    except Exception as e:
        print(f"    ❌ Excepción: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 TESTING SISTEMA MULTI-JUGADOR v3.0 (Biblioteca Estándar)")
    print("=" * 70)
    
    # Test 1: Endpoints GET básicos
    print("\n📡 TEST 1: ENDPOINTS HTTP GET")
    print("-" * 50)
    
    get_endpoints = [
        ("/", "Endpoint principal"),
        ("/health", "Endpoint de salud"),
        ("/api/info", "Información de API"),
        ("/api/multiplayer/world/status", "Estado del mundo"),
        ("/api/multiplayer/players", "Lista de jugadores"),
        ("/api/multiplayer/sessions", "Sesiones activas"),
        ("/docs", "Documentación API")
    ]
    
    get_results = []
    for endpoint, description in get_endpoints:
        result = test_endpoint(endpoint, description)
        get_results.append(result)
        time.sleep(0.1)  # Pequeña pausa entre requests
    
    # Test 2: Endpoints POST
    print("\n📝 TEST 2: ENDPOINTS HTTP POST")
    print("-" * 50)
    
    post_tests = [
        ("/api/multiplayer/auth/login", 
         {"username": "test_player", "password": "test_password"}, 
         "Login de usuario"),
        ("/api/multiplayer/sessions/create", 
         {"player_name": "TestPlayer", "session_type": "adventure"}, 
         "Creación de sesión")
    ]
    
    post_results = []
    for endpoint, data, description in post_tests:
        result = test_post_endpoint(endpoint, data, description)
        post_results.append(result)
        time.sleep(0.1)
    
    # Test 3: Verificación de conectividad básica
    print("\n🔌 TEST 3: CONECTIVIDAD BÁSICA")
    print("-" * 50)
    
    try:
        # Test simple de conexión
        with urllib.request.urlopen("http://127.0.0.1:8002/", timeout=3) as response:
            if response.status == 200:
                print("  ✅ Servidor respondiendo correctamente")
                connectivity_ok = True
            else:
                print(f"  ❌ Servidor respondió con status {response.status}")
                connectivity_ok = False
    except Exception as e:
        print(f"  ❌ Error de conectividad: {e}")
        connectivity_ok = False
    
    # Resultados finales
    print("\n" + "=" * 70)
    print("📊 RESULTADOS FINALES")
    print("-" * 70)
    
    get_passed = sum(get_results)
    get_total = len(get_results)
    post_passed = sum(post_results)
    post_total = len(post_results)
    
    print(f"📡 Endpoints GET: {get_passed}/{get_total} ({get_passed/get_total*100:.1f}%)")
    print(f"📝 Endpoints POST: {post_passed}/{post_total} ({post_passed/post_total*100:.1f}%)")
    print(f"🔌 Conectividad: {'✅ OK' if connectivity_ok else '❌ FAIL'}")
    
    total_tests = get_total + post_total + 1
    total_passed = get_passed + post_passed + (1 if connectivity_ok else 0)
    
    print(f"\n🏆 TOTAL: {total_passed}/{total_tests} tests pasaron ({total_passed/total_tests*100:.1f}%)")
    
    if total_passed == total_tests:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Sistema multi-jugador completamente funcional")
        print("🚀 Listo para implementar WebSocket client")
    elif total_passed >= total_tests * 0.8:
        print("\n🟡 SISTEMA MAYORMENTE FUNCIONAL")
        print("✅ Funcionalidad básica operativa")
        print("💡 Algunos endpoints avanzados pueden necesitar ajustes")
    elif total_passed >= total_tests * 0.5:
        print("\n🟠 SISTEMA PARCIALMENTE FUNCIONAL")
        print("⚠️ Funcionalidad básica operativa con limitaciones")
        print("🔧 Revisar configuración de endpoints avanzados")
    else:
        print("\n🔴 SISTEMA CON PROBLEMAS")
        print("❌ Muchos tests fallaron")
        print("🛠️ Revisar configuración del servidor")
        print("💡 Verificar que el servidor esté corriendo en puerto 8002")
    
    # Recomendaciones
    print("\n💡 PRÓXIMOS PASOS:")
    if connectivity_ok:
        print("  1. ✅ Servidor básico funcional")
        if get_passed >= get_total * 0.8:
            print("  2. ✅ Endpoints GET funcionando bien")
            print("  3. 🔜 Proceder con testing de WebSocket")
            print("  4. 🔜 Implementar frontend multi-jugador")
        else:
            print("  2. 🔧 Revisar endpoints GET que fallan")
            print("  3. 🔜 Optimizar respuestas de API")
    else:
        print("  1. ❌ Verificar que el servidor esté corriendo")
        print("  2. 🔧 Revisar puerto 8002")
        print("  3. 🔧 Verificar logs del servidor")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        import traceback
        traceback.print_exc()
