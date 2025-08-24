"""
🚀 INICIO RÁPIDO - Adventure Game Web Interface Backend
Script para probar rápidamente el backend de la interfaz web
"""

import sys
import os
import subprocess
import asyncio
import time
from pathlib import Path

# Agregar directorio backend al path
backend_dir = Path(__file__).parent / "backend" / "app"
sys.path.append(str(backend_dir))

def print_banner():
    """Muestra banner del sistema"""
    print("""
🌐═══════════════════════════════════════════════════════════
   ADVENTURE GAME WEB INTERFACE v2.0.0
   Panel de Administración Profesional
═══════════════════════════════════════════════════════════🌐
""")

def check_dependencies():
    """Verifica dependencias del backend"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'websockets',
        'python-jose',
        'passlib',
        'python-multipart'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Faltan dependencias: {', '.join(missing)}")
        print("💡 Instalando dependencias...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing, check=True)
            print("✅ Dependencias instaladas")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias")
            return False
    
    print("✅ Todas las dependencias están disponibles")
    return True

def show_api_info():
    """Muestra información de la API"""
    print("""
📊 INFORMACIÓN DE LA API:

🌐 URLs PRINCIPALES:
   • Dashboard Principal: http://localhost:8000/
   • Documentación API: http://localhost:8000/docs
   • API Alternativa: http://localhost:8000/redoc
   • Health Check: http://localhost:8000/api/health
   • Métricas: http://localhost:8000/api/metrics

🔌 WEBSOCKET:
   • Tiempo Real: ws://localhost:8000/ws

🔐 AUTENTICACIÓN:
   • Método: JWT Bearer Token
   • Login: POST /api/auth/login
   
🔑 CREDENCIALES DE PRUEBA:
   • admin:admin123 (acceso completo)
   • operator:operator123 (lectura + backup)
   • viewer:viewer123 (solo lectura)

📡 ENDPOINTS PRINCIPALES:
   • GET /api/system/status - Estado del sistema
   • GET /api/backups - Lista de backups
   • POST /api/backups/create - Crear backup
   • GET /api/events - Eventos del juego
   • GET /api/metrics - Métricas en tiempo real
""")

def test_auth_system():
    """Prueba el sistema de autenticación"""
    print("🔐 Probando sistema de autenticación...")
    
    try:
        from auth import AuthManager, initialize_default_users
        
        # Inicializar usuarios
        initialize_default_users()
        
        # Probar login
        user = AuthManager.authenticate_user("admin", "admin123")
        if user:
            print("✅ Sistema de autenticación funcionando")
            token = AuthManager.create_access_token({"sub": "admin"})
            print(f"✅ Token JWT generado: {token[:30]}...")
            return True
        else:
            print("❌ Error en sistema de autenticación")
            return False
            
    except Exception as e:
        print(f"❌ Error probando autenticación: {e}")
        return False

def start_backend_server():
    """Inicia el servidor backend"""
    print("🚀 Iniciando servidor backend...")
    print("⏳ Presiona Ctrl+C para detener")
    print()
    
    try:
        # Cambiar al directorio backend
        backend_app_dir = Path(__file__).parent / "backend" / "app"
        os.chdir(backend_app_dir)
        
        # Iniciar servidor
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")

async def test_websocket():
    """Prueba conexión WebSocket"""
    try:
        import websockets
        import json
        
        print("🔌 Probando conexión WebSocket...")
        
        async with websockets.connect("ws://localhost:8000/ws") as websocket:
            # Recibir mensaje inicial
            initial_data = await websocket.recv()
            message = json.loads(initial_data)
            print(f"✅ WebSocket conectado: {message['type']}")
            
            # Enviar ping
            await websocket.send(json.dumps({"type": "ping"}))
            
            # Recibir pong
            pong_data = await websocket.recv()
            pong_message = json.loads(pong_data)
            if pong_message["type"] == "pong":
                print("✅ WebSocket ping/pong funcionando")
                return True
                
    except Exception as e:
        print(f"❌ Error probando WebSocket: {e}")
        return False

def quick_api_test():
    """Prueba rápida de la API"""
    print("🧪 Probando endpoints de la API...")
    
    try:
        import requests
        import time
        
        # Esperar a que el servidor esté listo
        print("⏳ Esperando servidor...")
        time.sleep(3)
        
        # Test health check
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check funcionando")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
        
        # Test documentación
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Documentación disponible en http://localhost:8000/docs")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error probando API: {e}")
        return False
    except ImportError:
        print("⚠️ requests no disponible, saltando test de API")
        return True

def main():
    """Función principal"""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Probar autenticación
    if not test_auth_system():
        return
    
    # Mostrar información
    show_api_info()
    
    # Preguntar si iniciar servidor
    start_server = input("\n🚀 ¿Iniciar servidor backend? [S/n]: ").strip().lower()
    
    if start_server not in ['n', 'no']:
        print("\n📋 INSTRUCCIONES:")
        print("1. El servidor se iniciará en http://localhost:8000")
        print("2. Visita http://localhost:8000/docs para ver la API")
        print("3. Usa las credenciales arriba para autenticarte")
        print("4. Presiona Ctrl+C para detener el servidor")
        print()
        
        # Iniciar servidor
        start_backend_server()
    else:
        print("✅ Configuración completada")
        print("💡 Para iniciar manualmente:")
        print("   cd web_interface/backend/app")
        print("   python -m uvicorn main:app --reload")

if __name__ == "__main__":
    main()
