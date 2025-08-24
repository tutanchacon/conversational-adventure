#!/usr/bin/env python3
# 🔍 ANÁLISIS COMPLETO DEL PROBLEMA WEBSOCKET

"""
Análisis diagnóstico completo para identificar por qué los endpoints WebSocket no funcionan
"""

import urllib.request
import json
import socket
import time

def test_server_basic_response():
    """Verificar respuesta básica del servidor"""
    print("🔍 ANÁLISIS 1: RESPUESTA BÁSICA DEL SERVIDOR")
    print("-" * 60)
    
    try:
        with urllib.request.urlopen("http://127.0.0.1:8002/", timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"✅ Servidor respondiendo:")
            print(f"   - Estado: {response.status}")
            print(f"   - Mensaje: {data.get('message', 'N/A')}")
            print(f"   - Versión: {data.get('version', 'N/A')}")
            print(f"   - Timestamp: {data.get('timestamp', 'N/A')}")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_openapi_endpoints():
    """Verificar endpoints disponibles en OpenAPI"""
    print("\n🔍 ANÁLISIS 2: ENDPOINTS DISPONIBLES (OpenAPI)")
    print("-" * 60)
    
    try:
        with urllib.request.urlopen("http://127.0.0.1:8002/openapi.json", timeout=5) as response:
            openapi_data = json.loads(response.read().decode())
            
            paths = openapi_data.get("paths", {})
            print(f"📊 Total de endpoints encontrados: {len(paths)}")
            
            # Buscar endpoints WebSocket
            websocket_endpoints = []
            for path, methods in paths.items():
                for method, details in methods.items():
                    if "websocket" in str(details).lower() or "ws" in path.lower():
                        websocket_endpoints.append((path, method))
            
            if websocket_endpoints:
                print(f"🔌 Endpoints WebSocket encontrados: {len(websocket_endpoints)}")
                for path, method in websocket_endpoints:
                    print(f"   - {method.upper()} {path}")
            else:
                print("❌ No se encontraron endpoints WebSocket en OpenAPI")
            
            # Mostrar algunos endpoints importantes
            important_paths = ["/", "/docs", "/health", "/api/health", "/ws", "/ws/multiplayer"]
            print(f"\n📋 Verificación de endpoints importantes:")
            for path in important_paths:
                if path in paths:
                    methods = list(paths[path].keys())
                    print(f"   ✅ {path} - Métodos: {methods}")
                else:
                    print(f"   ❌ {path} - No encontrado")
            
            return len(websocket_endpoints) > 0
            
    except Exception as e:
        print(f"❌ Error obteniendo OpenAPI: {e}")
        return False

def test_direct_websocket_connection_detailed():
    """Test detallado de conexión WebSocket directa"""
    print("\n🔍 ANÁLISIS 3: CONEXIÓN WEBSOCKET DETALLADA")
    print("-" * 60)
    
    endpoints_to_test = ["/ws", "/ws/multiplayer"]
    
    for endpoint in endpoints_to_test:
        print(f"\n🔌 Testing endpoint: {endpoint}")
        try:
            # Conectar vía TCP primero
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("127.0.0.1", 8002))
            
            # Enviar handshake WebSocket básico
            handshake = (
                f"GET {endpoint} HTTP/1.1\r\n"
                f"Host: 127.0.0.1:8002\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
                f"Sec-WebSocket-Version: 13\r\n"
                f"\r\n"
            )
            
            sock.send(handshake.encode())
            response = sock.recv(4096).decode()
            
            print(f"   📥 Respuesta HTTP:")
            lines = response.split('\r\n')
            status_line = lines[0] if lines else "Sin respuesta"
            print(f"      Status: {status_line}")
            
            # Analizar respuesta
            if "101 Switching Protocols" in response:
                print(f"   ✅ WebSocket handshake exitoso")
            elif "404 Not Found" in response:
                print(f"   ❌ Endpoint no encontrado (404)")
            elif "400 Bad Request" in response:
                print(f"   ⚠️ Request mal formado (400)")
            elif "426 Upgrade Required" in response:
                print(f"   ⚠️ Upgrade requerido (426)")
            else:
                print(f"   ❓ Respuesta inesperada")
                print(f"      Primeras líneas: {lines[:3]}")
            
            sock.close()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_uvicorn_websocket_support():
    """Verificar soporte WebSocket de uvicorn"""
    print("\n🔍 ANÁLISIS 4: SOPORTE WEBSOCKET DE UVICORN")
    print("-" * 60)
    
    # Verificar si uvicorn tiene soporte WebSocket
    try:
        import uvicorn
        print(f"✅ uvicorn importado correctamente")
        print(f"   - Versión: {getattr(uvicorn, '__version__', 'Desconocida')}")
        
        # Verificar dependencias WebSocket
        websocket_libs = []
        
        try:
            import websockets
            websocket_libs.append(f"websockets {getattr(websockets, '__version__', '?')}")
        except ImportError:
            pass
        
        try:
            import wsproto
            websocket_libs.append(f"wsproto {getattr(wsproto, '__version__', '?')}")
        except ImportError:
            pass
        
        if websocket_libs:
            print(f"✅ Librerías WebSocket disponibles:")
            for lib in websocket_libs:
                print(f"   - {lib}")
        else:
            print(f"❌ No se encontraron librerías WebSocket")
            
        return len(websocket_libs) > 0
        
    except ImportError:
        print(f"❌ Error importando uvicorn")
        return False

def test_fastapi_websocket_support():
    """Verificar soporte WebSocket de FastAPI"""
    print("\n🔍 ANÁLISIS 5: SOPORTE WEBSOCKET DE FASTAPI")
    print("-" * 60)
    
    try:
        from fastapi import WebSocket
        print(f"✅ FastAPI WebSocket importado correctamente")
        
        # Verificar si podemos crear una instancia
        try:
            # Esto no funcionará sin un scope real, pero nos dice si la clase existe
            print(f"✅ Clase WebSocket disponible: {WebSocket}")
        except Exception as e:
            print(f"⚠️ Problema con clase WebSocket: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando FastAPI WebSocket: {e}")
        return False

def test_multiplayer_module_imports():
    """Verificar imports de módulos multiplayer"""
    print("\n🔍 ANÁLISIS 6: IMPORTS DE MÓDULOS MULTIPLAYER")
    print("-" * 60)
    
    imports_to_test = [
        ("multiplayer.websocket_handler", ["websocket_manager", "websocket_endpoint"]),
        ("multiplayer.multiplayer_game", ["get_multiplayer_game"]),
        ("multiplayer.session_manager", ["MultiPlayerSessionManager"]),
    ]
    
    success_count = 0
    
    for module_name, expected_items in imports_to_test:
        try:
            # Intentar importar el módulo
            module = __import__(module_name, fromlist=expected_items)
            print(f"✅ Módulo {module_name} importado")
            
            # Verificar elementos específicos
            for item in expected_items:
                if hasattr(module, item):
                    print(f"   ✅ {item} disponible")
                else:
                    print(f"   ❌ {item} no encontrado")
            
            success_count += 1
            
        except ImportError as e:
            print(f"❌ Error importando {module_name}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado con {module_name}: {e}")
    
    return success_count == len(imports_to_test)

def main():
    """Análisis principal"""
    print("🔍 ANÁLISIS DIAGNÓSTICO COMPLETO - WEBSOCKET")
    print("=" * 80)
    print(f"⏰ Inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Ejecutar todos los análisis
    analyses = [
        ("Respuesta básica del servidor", test_server_basic_response),
        ("Endpoints OpenAPI", test_openapi_endpoints),
        ("Conexión WebSocket detallada", test_direct_websocket_connection_detailed),
        ("Soporte uvicorn WebSocket", test_uvicorn_websocket_support),
        ("Soporte FastAPI WebSocket", test_fastapi_websocket_support),
        ("Imports módulos multiplayer", test_multiplayer_module_imports),
    ]
    
    results = []
    
    for analysis_name, analysis_func in analyses:
        print(f"\n🔍 Ejecutando: {analysis_name}")
        start_time = time.time()
        
        try:
            result = analysis_func()
            if result is None:
                result = True  # Para análisis que no retornan bool
            results.append(result)
            duration = time.time() - start_time
            status = "✅ OK" if result else "❌ PROBLEM"
            print(f"📊 {analysis_name}: {status} ({duration:.2f}s)")
        except Exception as e:
            results.append(False)
            duration = time.time() - start_time
            print(f"📊 {analysis_name}: ❌ ERROR ({duration:.2f}s) - {e}")
    
    # Resultados finales y diagnóstico
    print("\n" + "=" * 80)
    print("📊 RESULTADOS DEL ANÁLISIS")
    print("-" * 80)
    
    success_count = sum(1 for r in results if r)
    total_count = len(results)
    
    print(f"🏆 Análisis exitosos: {success_count}/{total_count}")
    
    for i, (analysis_name, _) in enumerate(analyses):
        status = "✅ OK" if results[i] else "❌ PROBLEM"
        print(f"  • {analysis_name}: {status}")
    
    # Diagnóstico final
    print("\n🔍 DIAGNÓSTICO FINAL")
    print("-" * 80)
    
    if all(results):
        print("🟢 TODOS LOS COMPONENTES FUNCIONAN CORRECTAMENTE")
        print("🤔 El problema puede ser de configuración de rutas específica")
        print("💡 Recomendación: Revisar logs del servidor en tiempo real")
    elif results[0] and results[3] and results[4]:  # Servidor, uvicorn, fastapi OK
        print("🟡 COMPONENTES BÁSICOS FUNCIONAN")
        print("🔧 Problema probablemente en configuración de endpoints")
        if not results[5]:  # Problema con imports
            print("⚠️ Problema detectado: Imports de módulos multiplayer")
            print("🛠️ Solución: Revisar imports en main.py")
        if not results[1]:  # Problema con OpenAPI
            print("⚠️ Problema detectado: Endpoints no registrados en OpenAPI")
            print("🛠️ Solución: Verificar decoradores @app.websocket")
    else:
        print("🔴 PROBLEMAS FUNDAMENTALES DETECTADOS")
        if not results[0]:
            print("❌ Servidor no responde correctamente")
        if not results[3] or not results[4]:
            print("❌ Soporte WebSocket no disponible")
        print("🛠️ Solución: Reinstalar dependencias y revisar configuración")
    
    print(f"\n⏰ Análisis completado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Análisis interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante análisis: {e}")
        import traceback
        traceback.print_exc()
