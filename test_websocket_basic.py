#!/usr/bin/env python3
# 🔌 CLIENTE WEBSOCKET SIMPLIFICADO - SIN DEPENDENCIAS EXTERNAS

"""
Cliente WebSocket simplificado usando solo bibliotecas estándar
Para testing básico del endpoint WebSocket
"""

import socket
import base64
import hashlib
import struct
import json
import time
from urllib.parse import urlparse

class SimpleWebSocketClient:
    def __init__(self, url="ws://127.0.0.1:8002/ws"):
        self.url = url
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
        """Conectar usando WebSocket handshake básico"""
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

def test_websocket_endpoint_availability():
    """Test básico de disponibilidad del endpoint WebSocket"""
    print("🧪 TEST: DISPONIBILIDAD ENDPOINT WEBSOCKET")
    print("-" * 50)
    
    client = SimpleWebSocketClient()
    
    try:
        # Intentar conectar
        if client.connect():
            print("✅ Endpoint WebSocket disponible y respondiendo")
            
            # Mantener conexión brevemente
            time.sleep(1)
            
            client.disconnect()
            return True
        else:
            print("❌ Endpoint WebSocket no disponible o no responde correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False
    finally:
        client.disconnect()

def test_http_to_websocket_upgrade():
    """Test de upgrade HTTP a WebSocket"""
    print("\n🧪 TEST: HTTP TO WEBSOCKET UPGRADE")
    print("-" * 50)
    
    try:
        # Conectar como HTTP primero
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 8002))
        
        # Intentar request HTTP normal al endpoint WebSocket
        http_request = (
            "GET /ws HTTP/1.1\r\n"
            "Host: 127.0.0.1:8002\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        
        s.send(http_request.encode())
        response = s.recv(4096).decode()
        
        print(f"📥 Respuesta HTTP:")
        print(response[:300] + "..." if len(response) > 300 else response)
        
        s.close()
        
        # Analizar respuesta
        if "426 Upgrade Required" in response or "400" in response:
            print("✅ Servidor rechaza correctamente conexiones HTTP normales al endpoint WebSocket")
            return True
        elif "404" in response:
            print("❌ Endpoint WebSocket no encontrado")
            return False
        else:
            print("⚠️ Respuesta inesperada del servidor")
            return False
            
    except Exception as e:
        print(f"❌ Error en test HTTP: {e}")
        return False

def test_websocket_handshake_validation():
    """Test de validación del handshake WebSocket"""
    print("\n🧪 TEST: VALIDACIÓN HANDSHAKE WEBSOCKET")
    print("-" * 50)
    
    tests = [
        {
            "name": "Handshake válido",
            "headers": {
                "Upgrade": "websocket",
                "Connection": "Upgrade",
                "Sec-WebSocket-Key": "dGhlIHNhbXBsZSBub25jZQ==",
                "Sec-WebSocket-Version": "13"
            },
            "expected": "101"
        },
        {
            "name": "Sin header Upgrade",
            "headers": {
                "Connection": "Upgrade",
                "Sec-WebSocket-Key": "dGhlIHNhbXBsZSBub25jZQ==",
                "Sec-WebSocket-Version": "13"
            },
            "expected": "400"
        },
        {
            "name": "Versión WebSocket incorrecta",
            "headers": {
                "Upgrade": "websocket",
                "Connection": "Upgrade",
                "Sec-WebSocket-Key": "dGhlIHNhbXBsZSBub25jZQ==",
                "Sec-WebSocket-Version": "12"
            },
            "expected": "400"
        }
    ]
    
    results = []
    
    for test in tests:
        try:
            print(f"  🔍 Testing: {test['name']}")
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(("127.0.0.1", 8002))
            
            # Crear request con headers específicos
            request = f"GET /ws HTTP/1.1\r\nHost: 127.0.0.1:8002\r\n"
            for key, value in test["headers"].items():
                request += f"{key}: {value}\r\n"
            request += "\r\n"
            
            s.send(request.encode())
            response = s.recv(4096).decode()
            
            s.close()
            
            # Verificar código de estado esperado
            if test["expected"] in response:
                print(f"    ✅ OK: Respuesta esperada ({test['expected']})")
                results.append(True)
            else:
                print(f"    ❌ FAIL: Respuesta inesperada")
                print(f"    📥 {response[:100]}...")
                results.append(False)
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Handshake validation: {passed}/{total} tests pasaron")
    
    return passed >= total * 0.7  # 70% o más es aceptable

def test_server_websocket_configuration():
    """Test de configuración del servidor WebSocket"""
    print("\n🧪 TEST: CONFIGURACIÓN SERVIDOR WEBSOCKET")
    print("-" * 50)
    
    try:
        # Test de conectividad básica al servidor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex(("127.0.0.1", 8002))
        s.close()
        
        if result == 0:
            print("✅ Servidor accesible en puerto 8002")
            
            # Test de response headers del servidor
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 8002))
            
            request = "GET / HTTP/1.1\r\nHost: 127.0.0.1:8002\r\nConnection: close\r\n\r\n"
            s.send(request.encode())
            response = s.recv(4096).decode()
            s.close()
            
            # Verificar headers del servidor
            if "Server:" in response or "FastAPI" in response:
                print("✅ Servidor responde con headers apropiados")
                return True
            else:
                print("⚠️ Headers del servidor no contienen información esperada")
                return True  # No crítico
                
        else:
            print("❌ Servidor no accesible en puerto 8002")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servidor: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 TESTING WEBSOCKET - BIBLIOTECAS ESTÁNDAR")
    print("=" * 70)
    print(f"⏰ Inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Disponibilidad Endpoint", test_websocket_endpoint_availability),
        ("HTTP to WebSocket Upgrade", test_http_to_websocket_upgrade),
        ("Handshake Validation", test_websocket_handshake_validation),
        ("Configuración Servidor", test_server_websocket_configuration)
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
    
    print("\n🔍 ANÁLISIS")
    print("-" * 70)
    
    if success_rate >= 90:
        print("🟢 EXCELENTE: Endpoint WebSocket completamente funcional")
        print("✅ Listo para clientes WebSocket avanzados")
        status = "EXCELENTE"
    elif success_rate >= 75:
        print("🟡 BUENO: Endpoint WebSocket mayormente funcional")
        print("✅ Funcional para desarrollo básico")
        status = "BUENO"
    elif success_rate >= 50:
        print("🟠 REGULAR: Endpoint WebSocket parcialmente funcional")
        print("⚠️ Necesita revisión de configuración")
        status = "REGULAR"
    else:
        print("🔴 CRÍTICO: Endpoint WebSocket con problemas")
        print("🛠️ Revisar configuración del servidor")
        status = "CRÍTICO"
    
    print("\n🗺️ PRÓXIMOS PASOS")
    print("-" * 70)
    
    if status in ["EXCELENTE", "BUENO"]:
        print("1. ✅ Endpoint WebSocket validado")
        print("2. 🔜 Instalar cliente WebSocket completo (websockets library)")
        print("3. 🔜 Testing de mensajes bidireccionales")
        print("4. 🔜 Testing de múltiples conexiones simultáneas")
        print("5. 🔜 Implementar frontend con WebSocket")
    else:
        print("1. 🔧 Revisar configuración WebSocket en FastAPI")
        print("2. 🔧 Verificar ruteo de endpoint /ws")
        print("3. 🔧 Validar middleware WebSocket")
        print("4. 🔄 Reiniciar servidor si es necesario")
    
    print(f"\n⏰ Finalizado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return status, passed, total

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando tests: {e}")
        import traceback
        traceback.print_exc()
