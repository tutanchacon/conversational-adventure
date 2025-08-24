#!/usr/bin/env python3
# 🔌 CLIENTE WEBSOCKET SIMPLE

"""
Cliente WebSocket simple usando la librería websockets
"""

import asyncio
import websockets
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_websocket_simple():
    """Test básico de WebSocket"""
    print("🔌 CLIENTE WEBSOCKET SIMPLE")
    print("=" * 50)
    
    # Test endpoint básico /ws
    print("\n1. Testing /ws endpoint")
    try:
        uri = "ws://localhost:8000/ws"
        async with websockets.connect(uri, timeout=10) as websocket:
            print(f"✅ Conectado a {uri}")
            
            # Esperar mensaje inicial
            try:
                initial_message = await asyncio.wait_for(websocket.recv(), timeout=5)
                data = json.loads(initial_message)
                print(f"📥 Mensaje inicial recibido:")
                print(f"   Tipo: {data.get('type')}")
                print(f"   Timestamp: {data.get('timestamp')}")
                
                # Enviar un mensaje de prueba
                test_message = {
                    "type": "test",
                    "message": "Hola desde cliente WebSocket"
                }
                await websocket.send(json.dumps(test_message))
                print(f"📤 Mensaje enviado: {test_message}")
                
                # Intentar recibir respuesta
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=3)
                    print(f"📥 Respuesta: {response}")
                except asyncio.TimeoutError:
                    print(f"⏰ No hubo respuesta (timeout)")
                    
            except asyncio.TimeoutError:
                print(f"⏰ No se recibió mensaje inicial")
            
    except Exception as e:
        print(f"❌ Error conectando a /ws: {e}")
    
    # Test endpoint multiplayer /ws/multiplayer
    print("\n2. Testing /ws/multiplayer endpoint")
    try:
        uri = "ws://localhost:8000/ws/multiplayer"
        async with websockets.connect(uri, timeout=10) as websocket:
            print(f"✅ Conectado a {uri}")
            
            # Enviar mensaje de autenticación
            auth_message = {
                "type": "authenticate",
                "player_name": "TestPlayer",
                "session_id": "test-session-123"
            }
            await websocket.send(json.dumps(auth_message))
            print(f"📤 Mensaje de auth enviado: {auth_message}")
            
            # Esperar respuesta
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                data = json.loads(response)
                print(f"📥 Respuesta de auth:")
                print(f"   Tipo: {data.get('type')}")
                print(f"   Status: {data.get('status')}")
                print(f"   Message: {data.get('message')}")
            except asyncio.TimeoutError:
                print(f"⏰ No hubo respuesta de auth")
                
    except Exception as e:
        print(f"❌ Error conectando a /ws/multiplayer: {e}")

async def test_websocket_manual():
    """Test manual con más control"""
    print(f"\n🔧 TEST MANUAL WEBSOCKET")
    print("-" * 50)
    
    try:
        uri = "ws://localhost:8000/ws"
        websocket = await websockets.connect(uri)
        print(f"✅ Conexión manual establecida")
        
        # Mantener conexión activa por unos segundos
        for i in range(3):
            try:
                # Intentar recibir cualquier mensaje
                message = await asyncio.wait_for(websocket.recv(), timeout=2)
                print(f"📥 Mensaje {i+1}: {message}")
            except asyncio.TimeoutError:
                print(f"⏰ Timeout esperando mensaje {i+1}")
            except Exception as e:
                print(f"❌ Error recibiendo mensaje {i+1}: {e}")
                break
        
        await websocket.close()
        print(f"🔚 Conexión cerrada")
        
    except Exception as e:
        print(f"❌ Error en test manual: {e}")

async def main():
    """Función principal"""
    print("🚀 INICIANDO TESTS DE WEBSOCKET")
    print("=" * 60)
    
    await test_websocket_simple()
    await test_websocket_manual()
    
    print(f"\n✅ Tests completados")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n⚠️ Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en main: {e}")
        import traceback
        traceback.print_exc()
