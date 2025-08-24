@echo off
echo 🎨 ADVENTURE GAME - INSTALACIÓN FRONTEND REACT
echo ==============================================

REM Cambiar al directorio del frontend
cd /d "%~dp0frontend"

REM Verificar si Node.js está instalado
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js/npm no está instalado
    echo 💡 Instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js detectado
node --version
echo ✅ npm detectado  
npm --version

REM Instalar dependencias
echo.
echo 📦 Instalando dependencias...
npm install

if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente

echo.
echo 🚀 Iniciando servidor de desarrollo...
echo 📊 Frontend se abrirá en: http://localhost:3000
echo 🔌 Backend debe estar ejecutándose en: http://localhost:8001
echo.
echo 💡 INSTRUCCIONES:
echo 1. Asegúrate de que el backend esté ejecutándose:
echo    python .\web_interface\backend\app\demo_server.py
echo 2. El frontend se conectará automáticamente al backend
echo 3. Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar servidor de desarrollo
npm run dev

pause
