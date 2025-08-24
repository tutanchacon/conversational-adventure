#!/usr/bin/env python3
"""
🚀 INICIO RÁPIDO DEL ADVENTURE GAME v2.0.0
Inicia el servidor web para jugar en el browser
"""

import os
import sys
import uvicorn
from pathlib import Path

def start_server():
    print("🎮 ADVENTURE GAME v2.0.0 - INICIO RÁPIDO")
    print("=" * 50)
    
    # Cambiar al directorio correcto
    backend_dir = Path(__file__).parent / "web_interface" / "backend"
    if not backend_dir.exists():
        print("❌ No se encuentra el directorio backend")
        return
    
    os.chdir(str(backend_dir))
    sys.path.insert(0, str(backend_dir))
    
    print("📂 Directorio:", os.getcwd())
    print("🚀 Iniciando servidor FastAPI...")
    print("🌐 URL: http://localhost:8003")
    print("📱 Abre Chrome y ve a: http://localhost:8003")
    print("⏹️  Para parar: Ctrl+C")
    print("-" * 50)
    
    try:
        # Importar la app
        from app.main import app
        
        # Iniciar servidor
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8003,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        print("💡 Ejecuta desde el directorio principal del proyecto")

if __name__ == "__main__":
    start_server()
