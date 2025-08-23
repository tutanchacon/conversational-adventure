# Script de instalación completa y verificación
# Ejecuta este script para configurar todo el entorno

import subprocess
import sys
import os
import platform
from pathlib import Path

class AdventureGameSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.python_exe = self._get_python_executable()
        
    def _get_python_executable(self):
        """Determina el ejecutable de Python correcto"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
    
    def _get_pip_executable(self):
        """Determina el ejecutable de pip correcto"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:
            return self.venv_path / "bin" / "pip"
    
    def create_virtual_environment(self):
        """Crea el entorno virtual"""
        print("🔧 Creando entorno virtual...")
        
        if self.venv_path.exists():
            print("✅ Entorno virtual ya existe")
            return True
        
        try:
            subprocess.run([
                sys.executable, "-m", "venv", str(self.venv_path)
            ], check=True)
            print("✅ Entorno virtual creado")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creando entorno virtual: {e}")
            return False
    
    def install_dependencies(self):
        """Instala las dependencias del proyecto"""
        print("📦 Instalando dependencias...")
        
        pip_exe = self._get_pip_executable()
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ Archivo requirements.txt no encontrado")
            return False
        
        try:
            # Actualizar pip primero
            subprocess.run([
                str(pip_exe), "install", "--upgrade", "pip"
            ], check=True)
            
            # Instalar dependencias
            subprocess.run([
                str(pip_exe), "install", "-r", str(requirements_file)
            ], check=True)
            
            print("✅ Dependencias instaladas")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    
    def test_basic_functionality(self):
        """Prueba la funcionalidad básica"""
        print("🧪 Probando funcionalidad básica...")
        
        try:
            # Probar sistema de memoria
            result = subprocess.run([
                str(self.python_exe), "memory_system.py"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Sistema de memoria funcionando")
            else:
                print(f"❌ Error en sistema de memoria: {result.stderr}")
                return False
            
            # Probar integración MCP
            result = subprocess.run([
                str(self.python_exe), "mcp_integration.py"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Integración MCP funcionando")
            else:
                print(f"❌ Error en integración MCP: {result.stderr}")
                return False
            
            # Probar juego básico
            result = subprocess.run([
                str(self.python_exe), "test_game.py"
            ], cwd=self.project_root, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ Juego básico funcionando")
            else:
                print(f"❌ Error en juego: {result.stderr}")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Timeout en pruebas")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando pruebas: {e}")
            return False
    
    def check_ollama(self):
        """Verifica si Ollama está disponible"""
        print("🤖 Verificando Ollama...")
        
        try:
            import urllib.request
            import json
            
            with urllib.request.urlopen("http://localhost:11434/api/version", timeout=5) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode())
                    print(f"✅ Ollama disponible - Versión: {data.get('version', 'desconocida')}")
                    return True
                else:
                    print("⚠️ Ollama responde con error")
                    return False
                    
        except Exception:
            print("⚠️ Ollama no detectado")
            print("💡 Para experiencia completa:")
            print("   1. Instalar: curl -fsSL https://ollama.com/install.sh | sh")
            print("   2. Ejecutar: ollama serve")
            print("   3. Instalar modelo: ollama pull llama3.2")
            return False
    
    def create_run_scripts(self):
        """Crea scripts de ejecución convenientes"""
        print("📜 Creando scripts de ejecución...")
        
        # Script para Windows
        if platform.system() == "Windows":
            run_demo_bat = self.project_root / "run_demo.bat"
            with open(run_demo_bat, "w") as f:
                f.write(f"""@echo off
echo 🎮 Ejecutando demo del Adventure Game
cd /d "{self.project_root}"
call venv\\Scripts\\activate.bat
python demo_game.py
pause
""")
            
            run_test_bat = self.project_root / "run_test.bat"
            with open(run_test_bat, "w") as f:
                f.write(f"""@echo off
echo 🧪 Ejecutando pruebas del Adventure Game
cd /d "{self.project_root}"
call venv\\Scripts\\activate.bat
python test_game.py
pause
""")
        
        # Script para Unix/Linux/Mac
        else:
            run_demo_sh = self.project_root / "run_demo.sh"
            with open(run_demo_sh, "w") as f:
                f.write(f"""#!/bin/bash
echo "🎮 Ejecutando demo del Adventure Game"
cd "{self.project_root}"
source venv/bin/activate
python demo_game.py
""")
            os.chmod(run_demo_sh, 0o755)
            
            run_test_sh = self.project_root / "run_test.sh"
            with open(run_test_sh, "w") as f:
                f.write(f"""#!/bin/bash
echo "🧪 Ejecutando pruebas del Adventure Game"
cd "{self.project_root}"
source venv/bin/activate
python test_game.py
""")
            os.chmod(run_test_sh, 0o755)
        
        print("✅ Scripts de ejecución creados")
    
    def setup_complete(self):
        """Configuración completa"""
        print("\n" + "=" * 60)
        print("🎉 ¡CONFIGURACIÓN COMPLETA!")
        print("=" * 60)
        
        print("\n🚀 OPCIONES PARA EJECUTAR:")
        
        if platform.system() == "Windows":
            print("   📜 Demo completo:     run_demo.bat")
            print("   🧪 Prueba básica:     run_test.bat")
            print("   🎮 Manual:           venv\\Scripts\\activate && python demo_game.py")
        else:
            print("   📜 Demo completo:     ./run_demo.sh")
            print("   🧪 Prueba básica:     ./run_test.sh")
            print("   🎮 Manual:           source venv/bin/activate && python demo_game.py")
        
        print("\n🌟 CARACTERÍSTICAS:")
        print("   🧠 Memoria perfecta - NUNCA olvida nada")
        print("   🔨 El martillo que dejes estará ahí en 6 meses")
        print("   📊 Cada acción registrada con timestamp")
        print("   🤖 IA con contexto completo del mundo")
        print("   💾 Persistencia garantizada entre sesiones")
        
        print("\n📚 DOCUMENTACIÓN:")
        print("   📖 README.md - Documentación completa")
        print("   🔧 Troubleshooting incluido")
        print("   💡 Ejemplos de uso detallados")
        
        print("\n✨ ¡Disfruta tu aventura con memoria perfecta!")
    
    def run_setup(self):
        """Ejecuta la configuración completa"""
        print("🎯 CONFIGURACIÓN DEL ADVENTURE GAME")
        print("🧠 Con Sistema de Memoria Perfecta y MCP")
        print("=" * 60)
        
        success = True
        
        # Crear entorno virtual
        if not self.create_virtual_environment():
            success = False
        
        # Instalar dependencias
        if success and not self.install_dependencies():
            success = False
        
        # Probar funcionalidad
        if success and not self.test_basic_functionality():
            success = False
        
        # Verificar Ollama (no crítico)
        self.check_ollama()
        
        # Crear scripts de ejecución
        if success:
            self.create_run_scripts()
            self.setup_complete()
        else:
            print("\n❌ CONFIGURACIÓN INCOMPLETA")
            print("Revisa los errores anteriores y vuelve a intentar")
            return False
        
        return True

def main():
    """Función principal"""
    setup = AdventureGameSetup()
    success = setup.run_setup()
    
    if success:
        # Preguntar si quiere ejecutar demo
        try:
            response = input("\n¿Ejecutar demo ahora? (s/n): ").lower().strip()
            if response in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n🎮 Ejecutando demo...")
                subprocess.run([
                    str(setup.python_exe), "test_game.py"
                ], cwd=setup.project_root)
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
