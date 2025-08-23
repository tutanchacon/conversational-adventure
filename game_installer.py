# Instalador y Tester del Juego de Aventura con IA
# Ejecuta este script para verificar que todo funciona correctamente

import subprocess
import sys
import json
import os
from pathlib import Path
import urllib.request
import urllib.error

class GameInstaller:
    def __init__(self):
        self.required_packages = [
            "aiohttp",
            "numpy"
        ]
        self.ollama_models = [
            "llama3.2",
            "mistral", 
            "codellama"
        ]
    
    def check_python_version(self):
        """Verifica la versión de Python"""
        version = sys.version_info
        print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Se requiere Python 3.8 o superior")
            return False
        
        print("✅ Versión de Python compatible")
        return True
    
    def install_packages(self):
        """Instala paquetes requeridos"""
        print("\n📦 Verificando dependencias...")
        
        for package in self.required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package} ya instalado")
            except ImportError:
                print(f"📥 Instalando {package}...")
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", package
                    ])
                    print(f"✅ {package} instalado correctamente")
                except subprocess.CalledProcessError:
                    print(f"❌ Error instalando {package}")
                    return False
        
        return True
    
    def check_ollama_connection(self):
        """Verifica conexión con Ollama"""
        print("\n🤖 Verificando Ollama...")
        
        try:
            with urllib.request.urlopen("http://localhost:11434/api/version", timeout=5) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode())
                    print(f"✅ Ollama conectado - Versión: {data.get('version', 'desconocida')}")
                    return True
                else:
                    print(f"⚠️  Ollama responde pero con error: {response.getcode()}")
                    return False
        except Exception as e:
            print("❌ Ollama no está ejecutándose")
            print("💡 Para iniciarlo: 'ollama serve' en otra terminal")
            print("💡 Para instalarlo: curl -fsSL https://ollama.com/install.sh | sh")
            return False
    
    def check_available_models(self):
        """Verifica qué modelos están disponibles"""
        print("\n🧠 Verificando modelos disponibles...")
        
        try:
            with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=10) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode())
                    models = [model["name"] for model in data.get("models", [])]
                    
                    if models:
                        print("✅ Modelos disponibles:")
                        for model in models:
                            print(f"   📋 {model}")
                        return models[0]  # Retorna el primer modelo disponible
                    else:
                        print("⚠️  No hay modelos instalados")
                        print("💡 Para instalar: 'ollama pull llama3.2'")
                        return None
                else:
                    print("❌ Error obteniendo lista de modelos")
                    return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def test_ai_response(self, model_name):
        """Prueba una respuesta básica de la IA"""
        print(f"\n🧪 Probando respuesta de IA con {model_name}...")
        
        payload = json.dumps({
            "model": model_name,
            "prompt": "Responde brevemente: ¿Estás funcionando correctamente?",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 50
            }
        })
        
        try:
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=payload.encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode())
                    ai_response = result.get("response", "Sin respuesta")
                    print(f"🤖 IA responde: {ai_response.strip()}")
                    print("✅ IA funcionando correctamente")
                    return True
                else:
                    print(f"❌ Error: {response.getcode()}")
                    return False
        except Exception as e:
            print(f"❌ Error probando IA: {e}")
            return False
    
    def create_demo_script(self):
        """Crea script de demostración"""
        demo_script = '''
# Demo rápido del juego
import asyncio
from adventure_game import IntelligentAdventureGame, VectorMemoryProvider

async def demo():
    print("🎮 DEMO DEL JUEGO")
    print("================\\n")
    
    # Inicializar
    memory = VectorMemoryProvider("demo_game.db")
    game = IntelligentAdventureGame(memory, model="llama3.2")
    
    # Comandos de prueba
    test_commands = [
        "mirar alrededor",
        "examinar los libros",
        "tomar la llave oxidada",
        "ir al norte",
        "inventario"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\\n--- PRUEBA {i}/5 ---")
        print(f"🗣️ Jugador: {command}")
        
        try:
            response = await game.process_command_async(command)
            print(f"🎮 Juego: {response[:200]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        import time
        time.sleep(1)  # Pausa entre comandos
    
    print("\\n✅ Demo completada")
    await game.ollama.close()

if __name__ == "__main__":
    asyncio.run(demo())
'''
        
        with open("demo_game.py", "w", encoding="utf-8") as f:
            f.write(demo_script)
        
        print("✅ Script de demo creado: demo_game.py")
    
    def run_diagnostics(self):
        """Ejecuta diagnósticos completos"""
        print("🏥 DIAGNÓSTICO DEL SISTEMA")
        print("=" * 50)
        
        # Verificar Python
        if not self.check_python_version():
            return False
        
        # Instalar dependencias
        if not self.install_packages():
            return False
        
        # Verificar Ollama
        ollama_ok = self.check_ollama_connection()
        
        if ollama_ok:
            # Verificar modelos
            available_model = self.check_available_models()
            
            if available_model:
                # Probar IA
                ai_ok = self.test_ai_response(available_model)
                
                if ai_ok:
                    print("\n🎉 ¡TODO LISTO PARA JUGAR!")
                    print("📋 Ejecuta: python adventure_game.py")
                    
                    # Crear demo
                    self.create_demo_script()
                    print("🎮 O prueba: python demo_game.py")
                    
                    return True
        
        print("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        self.show_setup_instructions()
        return False
    
    def show_setup_instructions(self):
        """Muestra instrucciones de configuración"""
        print("\n📋 INSTRUCCIONES DE CONFIGURACIÓN:")
        print("1. Instalar Ollama:")
        print("   curl -fsSL https://ollama.com/install.sh | sh")
        print("\n2. Iniciar servidor Ollama:")
        print("   ollama serve")
        print("\n3. Instalar un modelo (en otra terminal):")
        print("   ollama pull llama3.2")
        print("\n4. Ejecutar el juego:")
        print("   python adventure_game.py")

def main():
    """Función principal del instalador"""
    installer = GameInstaller()
    
    print("🎯 INSTALADOR DEL JUEGO DE AVENTURA CON IA")
    print("🔧 Verificando sistema y dependencias...")
    print("-" * 50)
    
    success = installer.run_diagnostics()
    
    if success:
        print("\n🚀 ¡Listo para la aventura!")
        
        # Preguntar si quiere ejecutar demo
        try:
            response = input("\n¿Quieres ejecutar una demo rápida? (s/n): ").lower()
            if response in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n🎮 Iniciando demo...")
                os.system("python demo_game.py")
        except KeyboardInterrupt:
            print("\n👋 ¡Nos vemos!")

if __name__ == "__main__":
    main()
