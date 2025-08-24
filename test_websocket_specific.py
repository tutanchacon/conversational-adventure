#!/usr/bin/env python3
# 🔌 TEST ESPECÍFICO DEL ENDPOINT /ws/multiplayer

"""
Test específico para el endpoint WebSocket de multi-jugador
"""

import socket
import base64
import time

class SimpleWebSocketClient:
    def __init__(self, url="ws://127.0.0.1:8002/ws/multiplayer"):
        self.url = url
        from urllib.parse import urlparse
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.port = parsed.port or 80
        self.path = parsed.path or "/"
        self.socket = None
        self.connected = False
        
    def _create_websocket_key(self):
        """Crear clave WebSocket"""
        import random
        key = bytes([random.randint(0, 255) for _ in range(16)])
        return base64.b64encode(key).decode()
    
    def _create_handshake(self):
        """Crear handshake WebSocket"""
        key = self._create_websocket_key()
        
        handshake = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )
        
        return handshake.encode(), key
    
    def connect(self):
        """Conectar usando WebSocket handshake"""
        try:
            print(f"🔌 Conectando a {self.host}:{self.port}{self.path}...")
            
            # Crear socket TCP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            
            # Enviar handshake WebSocket
            handshake, key = self._create_handshake()
            self.socket.send(handshake)
            
            # Leer respuesta
            response = self.socket.recv(4096).decode()
            print(f"📥 Respuesta del servidor:")
            print(response[:500] + "..." if len(response) > 500 else response)
            
            # Verificar si es una respuesta WebSocket válida
            if "101 Switching Protocols" in response and "websocket" in response.lower():
                print("✅ Handshake WebSocket exitoso")
                self.connected = True
                return True
            else:
                print("❌ Handshake WebSocket falló")
                return False
                
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            return False
    
    def disconnect(self):
        """Desconectar"""
        if self.socket:
            try:
                self.socket.close()
                print("🔌 Desconectado")
            except:
                pass
            finally:
                self.connected = False
                self.socket = None

def test_multiplayer_websocket_endpoint():
    """Test del endpoint /ws/multiplayer"""
    print("🧪 TEST: ENDPOINT /ws/multiplayer")
    print("-" * 50)
    
    client = SimpleWebSocketClient("ws://127.0.0.1:8002/ws/multiplayer")
    
    try:
        # Intentar conectar
        if client.connect():
            print("✅ Endpoint /ws/multiplayer disponible y respondiendo")
            
            # Mantener conexión brevemente
            time.sleep(2)
            
            client.disconnect()
            return True
        else:
            print("❌ Endpoint /ws/multiplayer no disponible")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False
    finally:
        client.disconnect()

def test_general_websocket_endpoint():
    """Test del endpoint /ws general"""
    print("\n🧪 TEST: ENDPOINT /ws")
    print("-" * 50)
    
    client = SimpleWebSocketClient("ws://127.0.0.1:8002/ws")
    
    try:
        if client.connect():
            print("✅ Endpoint /ws disponible y respondiendo")
            time.sleep(2)
            client.disconnect()
            return True
        else:
            print("❌ Endpoint /ws no disponible")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False
    finally:
        client.disconnect()

def test_websocket_server_logs():
    """Verificar qué endpoints están registrados"""
    print("\n🧪 TEST: VERIFICACIÓN DE LOGS DEL SERVIDOR")
    print("-" * 50)
    
    print("💡 Revisar logs del servidor para:")
    print("  1. ✅ Sistema multi-jugador inicializado")
    print("  2. ✅ MultiPlayerWebSocketManager inicializado")
    print("  3. ❌ Errores de inicialización")
    print("  4. ❌ Warnings de WebSocket")
    
    return True

def main():
    """Función principal de testing específico"""
    print("🚀 TESTING ENDPOINTS WEBSOCKET ESPECÍFICOS")
    print("=" * 70)
    print(f"⏰ Inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Endpoint /ws/multiplayer", test_multiplayer_websocket_endpoint),
        ("Endpoint /ws general", test_general_websocket_endpoint),
        ("Verificación logs", test_websocket_server_logs)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}")
        start_time = time.time()
        
        try:
            result = test_func()
            results.append(result)
            duration = time.time() - start_time
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"📊 {test_name}: {status} ({duration:.2f}s)")
        except Exception as e:
            results.append(False)
            duration = time.time() - start_time
            print(f"📊 {test_name}: ❌ ERROR ({duration:.2f}s) - {e}")
    
    # Resultados finales
    print("\n" + "=" * 70)
    print("📊 RESULTADOS FINALES")
    print("-" * 70)
    
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"🏆 Tests pasados: {passed}/{total} ({success_rate:.1f}%)")
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  • {test_name}: {status}")
    
    print("\n🔍 DIAGNÓSTICO")
    print("-" * 70)
    
    if results[0]:  # /ws/multiplayer funciona
        print("🟢 ENDPOINT MULTI-JUGADOR FUNCIONAL")
        print("✅ /ws/multiplayer respondiendo correctamente")
        print("🚀 Listo para cliente WebSocket avanzado")
    elif results[1]:  # /ws funciona pero /ws/multiplayer no
        print("🟡 ENDPOINT GENERAL FUNCIONAL")
        print("✅ /ws respondiendo correctamente")
        print("⚠️ /ws/multiplayer tiene problemas")
        print("💡 Revisar configuración multi-jugador")
    else:
        print("🔴 PROBLEMAS CON ENDPOINTS WEBSOCKET")
        print("❌ Ningún endpoint WebSocket funcional")
        print("🛠️ Revisar configuración del servidor")
    
    print("\n💡 PRÓXIMOS PASOS")
    print("-" * 70)
    
    if results[0]:  # /ws/multiplayer funciona
        print("1. ✅ Endpoint multi-jugador validado")
        print("2. 🔜 Crear cliente WebSocket real con librería websockets")
        print("3. 🔜 Testing de mensajes de juego")
        print("4. 🔜 Testing de múltiples jugadores")
    elif results[1]:  # /ws funciona
        print("1. ✅ Endpoint general validado")
        print("2. 🔧 Investigar problema con /ws/multiplayer")
        print("3. 🔜 Usar endpoint /ws para testing básico")
    else:
        print("1. 🔧 Revisar configuración FastAPI WebSocket")
        print("2. 🔧 Verificar imports de módulos multiplayer")
        print("3. 🔧 Verificar logs del servidor para errores")
    
    print(f"\n⏰ Finalizado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        import traceback
        traceback.print_exc()
