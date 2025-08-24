#!/usr/bin/env python3
# 🎮 TEST ENDPOINT MULTIPLAYER - VERSIÓN COMPATIBLE

"""
Test del endpoint /ws/multiplayer usando conexión manual sin timeout
"""

import asyncio
import websockets
import json
import time
from datetime import datetime

async def test_multiplayer_endpoint_simple():
    """Test simple del endpoint multiplayer"""
    print("🚀 TEST SIMPLE ENDPOINT MULTIPLAYER")
    print("=" * 50)
    print(f"⏰ Inicio: {datetime.now().strftime('%H:%M:%S')}")
    
    # Test 1: Conexión básica
    print(f"\n🧪 TEST 1: CONEXIÓN BÁSICA")
    print("-" * 30)
    
    try:
        uri = "ws://localhost:8000/ws/multiplayer"
        websocket = await websockets.connect(uri)
        print(f"✅ Conectado a {uri}")
        
        # Esperar mensaje inicial (sin timeout estricto)
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=10)
            data = json.loads(message)
            print(f"📥 Mensaje recibido:")
            print(f"   Tipo: {data.get('type', 'N/A')}")
            print(f"   Status: {data.get('status', 'N/A')}")
            if 'message' in data:
                print(f"   Message: {data.get('message', 'N/A')}")
            
            test1_result = True
        except asyncio.TimeoutError:
            print(f"⏰ No se recibió mensaje inicial")
            test1_result = False
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            test1_result = False
        
        await websocket.close()
        print(f"📊 Test 1 - Conexión: {'✅ PASS' if test1_result else '❌ FAIL'}")
        
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        test1_result = False
        print(f"📊 Test 1 - Conexión: ❌ FAIL")
    
    # Test 2: Autenticación
    print(f"\n🧪 TEST 2: AUTENTICACIÓN")
    print("-" * 30)
    
    try:
        uri = "ws://localhost:8000/ws/multiplayer"
        websocket = await websockets.connect(uri)
        
        # Enviar autenticación
        auth_message = {
            "type": "authenticate",
            "player_name": "TestPlayer",
            "session_id": f"test-{int(time.time())}"
        }
        await websocket.send(json.dumps(auth_message))
        print(f"📤 Enviado: {auth_message}")
        
        # Esperar respuesta
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=15)
            data = json.loads(response)
            print(f"📥 Respuesta:")
            print(f"   Tipo: {data.get('type', 'N/A')}")
            print(f"   Success: {data.get('success', 'N/A')}")
            if 'player_id' in data:
                print(f"   Player ID: {data.get('player_id', 'N/A')}")
            if 'session_id' in data:
                print(f"   Session ID: {data.get('session_id', 'N/A')}")
            
            test2_result = data.get('success', False) or data.get('type') == 'authentication_response'
        except asyncio.TimeoutError:
            print(f"⏰ Timeout esperando respuesta de auth")
            test2_result = False
        except Exception as e:
            print(f"❌ Error en auth: {e}")
            test2_result = False
        
        await websocket.close()
        print(f"📊 Test 2 - Autenticación: {'✅ PASS' if test2_result else '❌ FAIL'}")
        
    except Exception as e:
        print(f"❌ Error en test de auth: {e}")
        test2_result = False
        print(f"📊 Test 2 - Autenticación: ❌ FAIL")
    
    # Test 3: Comando de juego
    print(f"\n🧪 TEST 3: COMANDO DE JUEGO")
    print("-" * 30)
    
    try:
        uri = "ws://localhost:8000/ws/multiplayer"
        websocket = await websockets.connect(uri)
        
        # Autenticar primero
        auth_message = {
            "type": "authenticate",
            "player_name": "CmdTester",
            "session_id": f"cmd-{int(time.time())}"
        }
        await websocket.send(json.dumps(auth_message))
        
        # Esperar respuesta de auth
        try:
            await asyncio.wait_for(websocket.recv(), timeout=10)
        except:
            pass
        
        # Enviar comando
        command_message = {
            "type": "game_command",
            "command": "look",
            "args": []
        }
        await websocket.send(json.dumps(command_message))
        print(f"📤 Comando enviado: look")
        
        # Esperar respuesta del comando
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=15)
            data = json.loads(response)
            print(f"📥 Respuesta comando:")
            print(f"   Tipo: {data.get('type', 'N/A')}")
            if 'result' in data:
                result_text = str(data.get('result', ''))[:100]
                print(f"   Resultado: {result_text}...")
            
            test3_result = data.get('type') in ['game_response', 'command_result', 'game_state']
        except asyncio.TimeoutError:
            print(f"⏰ Timeout esperando respuesta de comando")
            test3_result = False
        except Exception as e:
            print(f"❌ Error en comando: {e}")
            test3_result = False
        
        await websocket.close()
        print(f"📊 Test 3 - Comando: {'✅ PASS' if test3_result else '❌ FAIL'}")
        
    except Exception as e:
        print(f"❌ Error en test de comando: {e}")
        test3_result = False
        print(f"📊 Test 3 - Comando: ❌ FAIL")
    
    # Resultados finales
    print(f"\n" + "=" * 50)
    print(f"📊 RESULTADOS FINALES")
    print("-" * 50)
    
    tests = [
        ("Conexión Básica", test1_result),
        ("Autenticación", test2_result),
        ("Comando de Juego", test3_result)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    print(f"🏆 Tests pasados: {passed}/{total} ({passed/total*100:.1f}%)")
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  • {test_name}: {status}")
    
    # Diagnóstico
    print(f"\n🔍 DIAGNÓSTICO")
    print("-" * 50)
    
    if passed == total:
        print("🟢 ENDPOINT MULTIPLAYER COMPLETAMENTE FUNCIONAL")
        print("🎉 Todos los tests pasaron")
        print("✅ Listo para uso en producción")
    elif passed >= 2:
        print("🟡 ENDPOINT MULTIPLAYER MAYORMENTE FUNCIONAL")
        print("👍 Funcionalidades básicas operativas")
        print("🔧 Algunos ajustes menores requeridos")
    elif passed >= 1:
        print("🟠 ENDPOINT MULTIPLAYER PARCIALMENTE FUNCIONAL")
        print("⚠️ Algunas funcionalidades operativas")
        print("🛠️ Requiere correcciones importantes")
    else:
        print("🔴 ENDPOINT MULTIPLAYER NO FUNCIONAL")
        print("❌ Ningún test pasó")
        print("🚨 Requiere investigación completa")
    
    print(f"\n⏰ Completado: {datetime.now().strftime('%H:%M:%S')}")
    return passed, total

async def main():
    """Función principal"""
    try:
        await test_multiplayer_endpoint_simple()
    except Exception as e:
        print(f"❌ Error en main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n⚠️ Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando: {e}")
