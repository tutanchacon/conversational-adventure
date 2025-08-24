#!/usr/bin/env python3
"""
🔧 SETUP AI ENVIRONMENT - Adventure Game v3.0
Script para configurar el entorno de IA con todas las dependencias
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def print_banner():
    """Mostrar banner de instalación"""
    print("🧠 AI ADVENTURE GAME v3.0 - ENVIRONMENT SETUP")
    print("=" * 60)
    print("🚀 Setting up AI environment with all dependencies...")
    print("⚡ This will install: OpenAI, ChromaDB, spaCy, Transformers, and more")
    print("-" * 60)

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8+ required")
        return False
    
    print("✅ Python version compatible")
    return True

def check_venv():
    """Verificar si estamos en un entorno virtual"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✅ Virtual environment detected")
        return True
    else:
        print("⚠️  Warning: Not in virtual environment")
        print("   Recommendation: Create virtual environment first")
        print("   Command: python -m venv ai_env && ai_env\\Scripts\\activate")
        
        response = input("Continue anyway? (y/N): ").lower().strip()
        return response == 'y'

def install_package(package_name: str, description: str = "") -> bool:
    """Instalar un paquete con pip"""
    try:
        print(f"📦 Installing {package_name}{'(' + description + ')' if description else ''}...")
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {package_name} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package_name}")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception installing {package_name}: {e}")
        return False

def install_core_ai_packages():
    """Instalar paquetes core de IA"""
    print("\n🧠 INSTALLING CORE AI PACKAGES")
    print("-" * 40)
    
    core_packages = [
        ("openai>=1.0.0", "OpenAI GPT-4 integration"),
        ("chromadb>=0.4.0", "Vector database"),
        ("numpy>=1.24.0", "Numerical computations"),
        ("transformers>=4.30.0", "Hugging Face models"),
        ("sentence-transformers>=2.2.0", "Semantic embeddings"),
        ("spacy>=3.7.0", "Advanced NLP"),
        ("scikit-learn>=1.3.0", "ML utilities"),
        ("pandas>=2.0.0", "Data analysis")
    ]
    
    success_count = 0
    for package, description in core_packages:
        if install_package(package, description):
            success_count += 1
    
    print(f"\n📊 Core AI packages: {success_count}/{len(core_packages)} installed")
    return success_count == len(core_packages)

def install_web_packages():
    """Instalar paquetes para web interface"""
    print("\n🌐 INSTALLING WEB INTERFACE PACKAGES")
    print("-" * 40)
    
    web_packages = [
        ("fastapi>=0.103.0", "API framework"),
        ("uvicorn[standard]>=0.23.0", "ASGI server"),
        ("websockets>=11.0.0", "Real-time communication"),
        ("python-multipart>=0.0.6", "File uploads"),
        ("jinja2>=3.1.0", "Template engine"),
        ("aiofiles>=23.1.0", "Async file operations")
    ]
    
    success_count = 0
    for package, description in web_packages:
        if install_package(package, description):
            success_count += 1
    
    print(f"\n📊 Web packages: {success_count}/{len(web_packages)} installed")
    return success_count == len(web_packages)

def install_optional_packages():
    """Instalar paquetes opcionales"""
    print("\n🎯 INSTALLING OPTIONAL AI PACKAGES")
    print("-" * 40)
    print("These packages enhance AI capabilities but are not required")
    
    optional_packages = [
        ("torch", "PyTorch for deep learning"),
        ("openai-whisper", "Speech-to-Text"),
        ("pillow>=10.0.0", "Image processing"),
        ("matplotlib>=3.7.0", "Plotting"),
        ("plotly>=5.15.0", "Interactive charts"),
        ("streamlit>=1.25.0", "AI prototyping"),
        ("redis>=4.6.0", "Caching and queues")
    ]
    
    print("\nOptional packages available:")
    for i, (package, description) in enumerate(optional_packages, 1):
        print(f"  {i}. {package} - {description}")
    
    response = input("\nInstall optional packages? (y/N): ").lower().strip()
    if response != 'y':
        print("⏭️  Skipping optional packages")
        return True
    
    success_count = 0
    for package, description in optional_packages:
        if install_package(package, description):
            success_count += 1
    
    print(f"\n📊 Optional packages: {success_count}/{len(optional_packages)} installed")
    return True

def download_spacy_models():
    """Descargar modelos de spaCy"""
    print("\n🧠 DOWNLOADING SPACY LANGUAGE MODELS")
    print("-" * 40)
    
    models = ["en_core_web_sm", "en_core_web_md"]
    
    for model in models:
        try:
            print(f"📥 Downloading {model}...")
            result = subprocess.run([
                sys.executable, "-m", "spacy", "download", model
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {model} downloaded successfully")
            else:
                print(f"❌ Failed to download {model}")
                print(f"   You can download manually: python -m spacy download {model}")
                
        except Exception as e:
            print(f"❌ Exception downloading {model}: {e}")
    
    return True

def create_env_file():
    """Crear archivo .env con configuración"""
    print("\n🔧 CREATING ENVIRONMENT CONFIGURATION")
    print("-" * 40)
    
    env_content = """# 🧠 AI ADVENTURE GAME v3.0 - ENVIRONMENT CONFIGURATION

# ===== OPENAI CONFIGURATION =====
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# ===== OPTIONAL AI SERVICES =====
# Anthropic Claude (optional)
ANTHROPIC_API_KEY=your_anthropic_key_here

# ElevenLabs for Text-to-Speech (optional)
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# ===== DATABASE CONFIGURATION =====
AI_DB_PATH=ai_adventure_game.db
VECTOR_DB_PATH=./ai_enhanced_memory

# ===== AI ENGINE SETTINGS =====
AI_DEFAULT_PERSONALITY=friendly
AI_ENABLE_PREDICTIONS=true
AI_ENABLE_VOICE=false
AI_RESPONSE_TIMEOUT=30

# ===== WEB SERVER SETTINGS =====
WEB_HOST=127.0.0.1
WEB_PORT=8091
DEBUG_MODE=false

# ===== LOGGING CONFIGURATION =====
LOG_LEVEL=INFO
LOG_FILE=ai_adventure.log

# ===== PERFORMANCE SETTINGS =====
MAX_CONCURRENT_REQUESTS=10
VECTOR_SEARCH_LIMIT=10
MEMORY_CACHE_SIZE=1000

# ===== SECURITY SETTINGS =====
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=*
"""
    
    env_path = Path(".env")
    
    if env_path.exists():
        response = input("📁 .env file already exists. Overwrite? (y/N): ").lower().strip()
        if response != 'y':
            print("⏭️  Keeping existing .env file")
            return True
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully")
        print("📝 Don't forget to add your OpenAI API key to the .env file!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_installations():
    """Probar que las instalaciones funcionan"""
    print("\n🧪 TESTING INSTALLATIONS")
    print("-" * 40)
    
    tests = [
        ("import openai", "OpenAI"),
        ("import chromadb", "ChromaDB"),
        ("import numpy", "NumPy"),
        ("import transformers", "Transformers"),
        ("import spacy", "spaCy"),
        ("import fastapi", "FastAPI"),
        ("import uvicorn", "Uvicorn")
    ]
    
    success_count = 0
    for test_code, package_name in tests:
        try:
            exec(test_code)
            print(f"✅ {package_name} import successful")
            success_count += 1
        except ImportError as e:
            print(f"❌ {package_name} import failed: {e}")
        except Exception as e:
            print(f"⚠️  {package_name} import error: {e}")
    
    print(f"\n📊 Import tests: {success_count}/{len(tests)} successful")
    return success_count >= len(tests) - 2  # Allow 2 failures

def create_startup_script():
    """Crear script de inicio"""
    print("\n🚀 CREATING STARTUP SCRIPTS")
    print("-" * 40)
    
    # Script de Python
    startup_content = '''#!/usr/bin/env python3
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
'''
    
    # Script de Windows
    batch_content = '''@echo off
echo 🧠 AI Adventure Game v3.0 - Quick Start
echo ================================
echo.
echo 🚀 Starting AI-enhanced server...
echo 🌐 URL: http://localhost:8091
echo 📱 Open browser and navigate to the URL above
echo ⏹️  To stop: Ctrl+C
echo.

python start_ai_game.py
pause
'''
    
    try:
        # Crear script Python
        with open("start_ai_game.py", 'w', encoding='utf-8') as f:
            f.write(startup_content)
        print("✅ start_ai_game.py created")
        
        # Crear script Windows
        with open("start_ai_game.bat", 'w', encoding='utf-8') as f:
            f.write(batch_content)
        print("✅ start_ai_game.bat created")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create startup scripts: {e}")
        return False

def show_final_instructions():
    """Mostrar instrucciones finales"""
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("🧠 AI Adventure Game v3.0 is ready to use!")
    print()
    print("📋 NEXT STEPS:")
    print("1. 🔑 Add your OpenAI API key to the .env file")
    print("2. 🚀 Run: python start_ai_game.py")
    print("3. 🌐 Open browser: http://localhost:8091")
    print("4. 🎮 Start your AI-enhanced adventure!")
    print()
    print("🎯 NEW AI FEATURES:")
    print("• 🧠 Smart AI narrator with perfect memory")
    print("• 🔍 Semantic search across all game history")
    print("• 🎭 Multiple AI personalities")
    print("• 🔮 Predictive gameplay suggestions")
    print("• 🎨 Dynamic content generation")
    print("• 🗣️ Natural language understanding")
    print()
    print("📚 For help and documentation:")
    print("• Check FASE3_AI_ENHANCEMENT_PLAN.md")
    print("• Visit the game interface for interactive help")
    print("• Use the 'help' command in-game")
    print()
    print("🎮 Happy AI-enhanced adventuring! 🚀")

def main():
    """Función principal de setup"""
    print_banner()
    
    # Verificar requisitos
    if not check_python_version():
        return False
    
    if not check_venv():
        return False
    
    print("\n🚀 Starting installation process...")
    
    # Instalar paquetes
    success_core = install_core_ai_packages()
    success_web = install_web_packages()
    install_optional_packages()
    
    # Descargar modelos
    download_spacy_models()
    
    # Crear configuración
    create_env_file()
    
    # Crear scripts de inicio
    create_startup_script()
    
    # Probar instalaciones
    success_tests = test_installations()
    
    # Mostrar resultado
    if success_core and success_web and success_tests:
        show_final_instructions()
        return True
    else:
        print("\n❌ SETUP INCOMPLETE")
        print("Some packages failed to install. Check the errors above.")
        print("You may need to install them manually.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
