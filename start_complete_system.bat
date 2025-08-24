@echo off
echo 🎮 ADVENTURE GAME v2.0 - SISTEMA COMPLETO
echo ==========================================

echo.
echo 🚀 Iniciando Adventure Game con Web Interface completa...
echo.

REM Verificar si Python está disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Instala Python desde: https://python.org
    pause
    exit /b 1
)

REM Verificar si Node.js está disponible
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js/npm no está instalado
    echo 💡 Instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python detectado: 
python --version
echo ✅ Node.js detectado:
node --version

echo.
echo 📦 CONFIGURACIÓN INICIAL
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🔄 Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ No se encontró entorno virtual
    echo 💡 Crea uno con: python -m venv venv
)

REM Instalar dependencias del backend si es necesario
echo 🔧 Verificando dependencias del backend...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando dependencias del backend...
    pip install -r requirements.txt
)

REM Instalar dependencias del frontend si es necesario
if not exist "web_interface\frontend\node_modules" (
    echo 📦 Instalando dependencias del frontend...
    cd web_interface\frontend
    npm install
    cd ..\..
)

echo.
echo 🎯 INICIANDO SERVICIOS
echo.

echo 📋 Se abrirán 2 ventanas:
echo    1. Backend Python (puerto 8001)
echo    2. Frontend React (puerto 3000)
echo.

echo 🔥 Presiona cualquier tecla para continuar...
pause >nul

REM Iniciar backend en nueva ventana
echo 🚀 Iniciando backend...
start "Adventure Game Backend" cmd /k "python .\web_interface\backend\app\demo_server.py"

REM Esperar un poco para que el backend se inicie
echo ⏳ Esperando backend...
timeout /t 3 >nul

REM Iniciar frontend en nueva ventana  
echo 🎨 Iniciando frontend...
start "Adventure Game Frontend" cmd /k "cd web_interface\frontend && npm run dev"

echo.
echo ✅ SISTEMA INICIADO CORRECTAMENTE!
echo.
echo 🌐 URLs disponibles:
echo    • Frontend Dashboard: http://localhost:3000
echo    • Backend API Docs: http://localhost:8001/docs
echo    • Backend Demo: http://localhost:8001
echo.
echo 📊 CARACTERÍSTICAS DISPONIBLES:
echo    ✅ Dashboard en tiempo real
echo    ✅ Gestión visual de backups  
echo    ✅ Sistema de memoria perfecta
echo    ✅ Vector search con ChromaDB
echo    ✅ WebSocket para actualizaciones live
echo    ✅ API REST completa
echo.
echo 🎮 ¡Disfruta tu Adventure Game con interface web profesional!
echo.
echo 💡 Para detener: Cierra las ventanas del backend y frontend
echo.

pause
