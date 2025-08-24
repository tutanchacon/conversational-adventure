#!/usr/bin/env python3
# 🧪 TEST DE CONECTIVIDAD DEL SERVIDOR MULTI-JUGADOR

import requests
import json

def test_http_connection():
    """Test básico de conexión HTTP"""
    print("🔍 Testing conexión HTTP al servidor...")
    
    try:
        response = requests.get("http://127.0.0.1:8002/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor HTTP funcionando:", data.get("message", "OK"))
            return True
        else:
            print("❌ Error en servidor HTTP:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error conectando al servidor HTTP:", e)
        return False

def test_health_endpoint():
    """Test del endpoint de salud"""
    print("🔍 Testing endpoint /health...")
    
    try:
        response = requests.get("http://127.0.0.1:8002/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint funcionando:", data)
            return True
        else:
            print("❌ Error en health endpoint:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error en health endpoint:", e)
        return False

def test_api_info():
    """Test del endpoint de información de API"""
    print("🔍 Testing endpoint /api/info...")
    
    try:
        response = requests.get("http://127.0.0.1:8002/api/info")
        if response.status_code == 200:
            data = response.json()
            print("✅ API Info:", data)
            return True
        else:
            print("❌ Error en API info:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error en API info:", e)
        return False

def test_multiplayer_endpoints():
    """Test de endpoints específicos de multi-jugador"""
    print("🔍 Testing endpoints multi-jugador...")
    
    try:
        # Test de estado del mundo
        response = requests.get("http://127.0.0.1:8002/api/multiplayer/world/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ World status:", data)
            return True
        else:
            print("❌ Error en world status:", response.status_code)
            return False
    except Exception as e:
        print("❌ Error en multiplayer endpoints:", e)
        return False

if __name__ == "__main__":
    print("🚀 TEST DE CONECTIVIDAD - SERVIDOR MULTI-JUGADOR")
    print("=" * 60)
    
    tests = [
        test_http_connection,
        test_health_endpoint,
        test_api_info,
        test_multiplayer_endpoints
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error ejecutando test {test.__name__}: {e}")
            results.append(False)
        print("-" * 40)
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"📊 RESULTADOS: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron! Servidor multi-jugador funcionando correctamente.")
        print("✅ Listo para continuar con tests de WebSocket.")
    else:
        print("⚠️ Algunos tests fallaron. Revisar la configuración del servidor.")
        print("💡 Verificar que el servidor esté corriendo en http://127.0.0.1:8002")
