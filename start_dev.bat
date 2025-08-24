@echo off
REM 🚀 SCRIPT DE INICIO AUTOMÁTICO PARA DESARROLLO
echo.
echo ========================================================
echo 🎮 ADVENTURE GAME - ENTORNO DE DESARROLLO
echo ========================================================
echo.

cd /d "D:\wamp64\www\conversational-adventure"

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Entorno virtual no encontrado
    echo 🔧 Creando entorno virtual...
    python -m venv venv
    echo ✅ Entorno virtual creado
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar dependencias
echo 🔍 Verificando dependencias...
pip list | findstr "fastapi" >nul
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo ✅ Entorno de desarrollo listo
echo 📁 Directorio: %CD%
echo 🐍 Python: 
python --version
echo.
echo 💡 Comandos útiles:
echo    • python main.py          - Ejecutar servidor principal
echo    • python test_*.py        - Ejecutar tests
echo    • pip install [paquete]   - Instalar dependencias
echo    • deactivate              - Salir del entorno virtual
echo.
echo ========================================================

REM Mantener la ventana abierta
cmd /k
