#!/usr/bin/env python3
# 🔍 TEST WEBSOCKET EN PUERTO CORRECTO

"""
Test rápido para verificar WebSocket en el puerto correcto (8000)
"""

import urllib.request
import socket
import json

def test_websocket_port_8000():
    """Test WebSocket en puerto 8000"""
    print("🔍 TESTING WEBSOCKET EN PUERTO 8000")
    print("-" * 50)
    
    # Primero verificar que el servidor responde
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/", timeout=5) as response:
            print(f"✅ Servidor responde en puerto 8000: {response.status}")
    except Exception as e:
        print(f"❌ Servidor no responde en puerto 8000: {e}")
        return False
    
    # Test endpoints WebSocket
    endpoints = ["/ws", "/ws/multiplayer"]
    
    for endpoint in endpoints:
        print(f"\n🔌 Testing: {endpoint}")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("127.0.0.1", 8000))
            
            handshake = (
                f"GET {endpoint} HTTP/1.1\r\n"
                f"Host: 127.0.0.1:8000\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
                f"Sec-WebSocket-Version: 13\r\n"
                f"\r\n"
            )
            
            sock.send(handshake.encode())
            response = sock.recv(4096).decode()
            
            print(f"   📥 Respuesta:")
            status_line = response.split('\r\n')[0]
            print(f"      {status_line}")
            
            if "101 Switching Protocols" in response:
                print(f"   ✅ WebSocket handshake EXITOSO")
            elif "404 Not Found" in response:
                print(f"   ❌ Endpoint no encontrado (404)")
            elif "503 Service Unavailable" in response:
                print(f"   ⚠️ Servicio no disponible (503)")
            else:
                print(f"   ❓ Respuesta inesperada")
            
            sock.close()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_openapi_port_8000():
    """Verificar OpenAPI en puerto 8000"""
    print(f"\n🔍 VERIFICANDO OPENAPI EN PUERTO 8000")
    print("-" * 50)
    
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/openapi.json", timeout=5) as response:
            data = json.loads(response.read().decode())
            paths = data.get("paths", {})
            
            print(f"📊 Total endpoints: {len(paths)}")
            
            # Buscar endpoints WebSocket
            for path, methods in paths.items():
                if "ws" in path.lower():
                    print(f"🔌 WebSocket endpoint encontrado: {path}")
                    for method in methods:
                        print(f"   - {method.upper()}")
                        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_websocket_port_8000()
    test_openapi_port_8000()
