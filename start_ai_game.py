#!/usr/bin/env python3
"""
🚀 AI Adventure Game v3.0 - Quick Start
"""

import os
import sys
from pathlib import Path

# Añadir directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar y ejecutar servidor
from ai_web_server import start_ai_server

if __name__ == "__main__":
    print("🧠 Starting AI Adventure Game v3.0...")
    
    # Verificar archivo .env
    if not Path(".env").exists():
        print("⚠️  Warning: .env file not found")
        print("   Create .env file and add your OpenAI API key")
    
    # Iniciar servidor
    start_ai_server(host="127.0.0.1", port=8091)
